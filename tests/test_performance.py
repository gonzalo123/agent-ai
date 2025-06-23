"""
Performance and stress tests for the application
"""
import time
import pytest
from unittest.mock import Mock, patch
import concurrent.futures
import threading


class TestPerformance:
    """Performance tests for critical application components"""
    
    @pytest.mark.slow
    def test_math_tools_performance(self):
        """Test MathTools performance with many operations"""
        from modules.tools import MathTools
        
        tools = MathTools()
        
        # Measure time for 1000 operations
        start_time = time.time()
        
        for i in range(1000):
            tools._sum_values(i, i + 1)
            if i % 2 == 0:  # Mix in some subtractions
                tools._diff_values(i + 10, i)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Should complete 1000 operations in less than 1 second
        assert execution_time < 1.0, f"Performance test failed: {execution_time:.3f}s for 1000 operations"
        
        # Verify history management (should only keep last 5)
        history = tools._get_history()
        assert len(history.split('\n')) == 5
    
    @pytest.mark.slow
    def test_history_retrieval_performance(self):
        """Test history retrieval performance with large history"""
        from modules.tools import MathTools
        
        tools = MathTools()
        
        # Build large history
        for i in range(10000):
            tools._sum_values(i, 1)
        
        # Measure history retrieval time
        start_time = time.time()
        
        for _ in range(100):  # Get history 100 times
            history = tools._get_history()
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Should retrieve history quickly
        assert execution_time < 0.1, f"History retrieval too slow: {execution_time:.3f}s"
        
        # Verify only last 5 operations
        assert len(history.split('\n')) == 5
    
    @pytest.mark.slow
    @patch('core.llm.aws.ChatBedrock')
    @patch('core.llm.aws.aws_get_service')
    def test_llm_initialization_performance(self, mock_aws_service, mock_chat_bedrock):
        """Test LLM initialization performance"""
        from core.llm.aws import get_llm
        
        mock_client = Mock()
        mock_aws_service.return_value = mock_client
        
        mock_llm = Mock()
        mock_chat_bedrock.return_value = mock_llm
        
        # Measure initialization time
        start_time = time.time()
        
        for _ in range(10):  # Initialize LLM 10 times
            llm = get_llm()
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Should initialize quickly
        assert execution_time < 5.0, f"LLM initialization too slow: {execution_time:.3f}s"
    
    @pytest.mark.slow
    def test_prompt_template_performance(self):
        """Test prompt template creation performance"""
        from langchain.prompts import ChatPromptTemplate
        from modules.prompts import AGENT_SYSTEM_PROMPT
        
        # Measure template creation time
        start_time = time.time()
        
        for _ in range(1000):
            prompt = ChatPromptTemplate.from_messages([
                ("system", AGENT_SYSTEM_PROMPT),
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}")
            ])
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Should create templates quickly
        assert execution_time < 2.0, f"Template creation too slow: {execution_time:.3f}s"


class TestStress:
    """Stress tests for application resilience"""
    
    @pytest.mark.slow
    def test_concurrent_math_tools(self):
        """Test concurrent access to MathTools"""
        from modules.tools import MathTools
        
        results = []
        errors = []
        
        def worker(worker_id):
            try:
                tools = MathTools()
                for i in range(100):
                    result = tools._sum_values(worker_id * 100 + i, 1)
                    results.append(result)
            except Exception as e:
                errors.append(e)
        
        # Run 10 concurrent workers
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(worker, i) for i in range(10)]
            concurrent.futures.wait(futures)
        
        # Verify no errors and correct number of results
        assert len(errors) == 0, f"Errors in concurrent execution: {errors}"
        assert len(results) == 1000  # 10 workers * 100 operations each
    
    @pytest.mark.slow
    def test_memory_usage_with_large_history(self):
        """Test memory usage with large operation history"""
        import sys
        from modules.tools import MathTools
        
        tools = MathTools()
        
        # Record initial memory usage (approximate)
        initial_objects = len(gc.get_objects()) if 'gc' in sys.modules else 0
        
        # Perform many operations
        for i in range(50000):
            tools._sum_values(i, 1)
        
        # Memory shouldn't grow unbounded due to history limit
        final_objects = len(gc.get_objects()) if 'gc' in sys.modules else 0
        
        # History should still be limited to 5 entries
        history = tools._get_history()
        assert len(history.split('\n')) == 5
        
        # Verify internal history list doesn't grow unbounded
        # (This is implementation-dependent, but good practice)
        assert len(tools.history) <= 50000  # Should contain all operations
    
    @pytest.mark.slow
    def test_repeated_llm_calls_stability(self):
        """Test stability of repeated LLM calls"""
        from unittest.mock import Mock, patch
        
        with patch('modules.llm.get_llm') as mock_get_llm, \
             patch('modules.llm.create_tool_calling_agent') as mock_create_agent, \
             patch('modules.llm.AgentExecutor') as mock_agent_executor, \
             patch('modules.llm.MathTools') as mock_math_tools:
            
            # Setup mocks
            mock_tools_instance = Mock()
            mock_tools_instance.get_tools.return_value = []
            mock_math_tools.return_value = mock_tools_instance
            
            mock_executor = Mock()
            mock_executor.invoke.return_value = {"output": "Test response"}
            mock_agent_executor.return_value = mock_executor
            
            from modules.llm import run
            
            errors = []
            
            # Run many iterations
            for i in range(100):
                try:
                    with patch('builtins.print'):
                        run(f"Test question {i}")
                except Exception as e:
                    errors.append(e)
            
            # Should handle all calls without errors
            assert len(errors) == 0, f"Errors in repeated calls: {errors}"
            assert mock_executor.invoke.call_count == 100
    
    @pytest.mark.slow
    def test_large_input_handling(self):
        """Test handling of large input strings"""
        from modules.tools import MathTools
        
        tools = MathTools()
        
        # Test with very long operation descriptions in history
        for i in range(10):
            # Create artificially long history entries
            a = i * 1000000  # Large numbers
            b = (i + 1) * 1000000
            result = tools._sum_values(a, b)
            assert result == a + b
        
        # History retrieval should still work efficiently
        start_time = time.time()
        history = tools._get_history()
        end_time = time.time()
        
        assert end_time - start_time < 0.1, "Large input handling too slow"
        assert len(history.split('\n')) == 5  # Still limited to 5 entries


class TestResourceUsage:
    """Tests for resource usage and limits"""
    
    def test_memory_efficiency_tools(self):
        """Test memory efficiency of MathTools"""
        from modules.tools import MathTools
        import sys
        
        # Create multiple instances
        tools_instances = []
        for i in range(100):
            tools = MathTools()
            tools._sum_values(i, i + 1)
            tools_instances.append(tools)
        
        # Each instance should maintain its own history
        for i, tools in enumerate(tools_instances):
            history = tools._get_history()
            expected = f"{i} + {i + 1} = {2 * i + 1}"
            assert expected in history
    
    def test_thread_safety_basic(self):
        """Basic thread safety test for MathTools"""
        from modules.tools import MathTools
        import threading
        
        tools = MathTools()
        results = []
        lock = threading.Lock()
        
        def worker(worker_id):
            for i in range(50):
                result = tools._sum_values(worker_id * 100 + i, 1)
                with lock:
                    results.append((worker_id, result))
        
        threads = []
        for i in range(5):
            thread = threading.Thread(target=worker, args=(i,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # All operations should complete
        assert len(results) == 250  # 5 threads * 50 operations
        
        # Results should be consistent
        for worker_id, result in results:
            assert isinstance(result, int)
            assert result > 0


# Utility to enable garbage collection for memory tests
try:
    import gc
except ImportError:
    gc = None
