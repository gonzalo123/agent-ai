# COPILOT EDITS OPERATIONAL GUIDELINES

## PRIME DIRECTIVE
- Avoid working on more than one file at a time.
- Multiple simultaneous edits to a file will cause corruption.
- Be chatting and teach about what you are doing while coding.
- Follow KISS principle (Keep It Simple, Stupid) and DRY (Don't Repeat Yourself).
- All source code MUST be written in English, including comments, variable names, function names, and documentation.
- All source code is in src folder. src folder is the only folder that will be copied to the docker image. 
- Use src as source code base folder. All imports should be relative to src folder.


## Command Line Interface (CLI) information
- Use **Click** library for CLI commands.
- CLI commands are located in `src/commands/` folder.
- Each command should have its own file in the `src/commands/` folder.
- The main CLI entry point is `src/cli.py`.
- The CLI commands should be registered in the `src/commands/__init__.py` file.
- The base path for cli scripts is `src/`
- use `cd src/` before running any CLI command.
- Use `python cli.py <command> <args>` to run CLI commands.

## LANGUAGE REQUIREMENTS - CRITICAL
- **ALL code comments, docstrings, and documentation MUST be written in English**
- **Variable names, function names, and identifiers MUST use English**
- **Error messages and log messages MUST be in English**
- **This applies regardless of the conversation language with the user**
- **Never translate technical terms or use mixed languages in code**
- **When user speaks in Spanish/other languages, respond in their language but keep ALL code in English**

## LARGE FILE & COMPLEX CHANGE PROTOCOL

### MAKING EDITS
- Focus on one conceptual change at a time
- Show clear "before" and "after" snippets when proposing changes
- Include concise explanations of what changed and why
- Always check if the edit maintains the project's coding style
- **Language**: All code comments and explanations MUST be in English

### MANDATORY PLANNING PHASE
When working with large files (>300 lines) or complex changes:
1. ALWAYS start by creating a detailed plan BEFORE making any edits
2. Your plan MUST include:
   - All functions/sections that need modification
   - The order in which changes should be applied
   - Dependencies between changes
   - Estimated number of separate edits required

3. Format your plan as:
## PROPOSED EDIT PLAN
Working with: [filename]
Total planned edits: [number]

### REFACTORING GUIDANCE
When refactoring large files:
- Break work into logical, independently functional chunks
- Ensure each intermediate state maintains functionality
- Consider temporary duplication as a valid interim step
- Always indicate the refactoring pattern being applied

### Edit sequence:
1. [First specific change] - Purpose: [why]
2. [Second specific change] - Purpose: [why]
3. Do you approve this plan? I'll proceed with Edit [number] after your confirmation.
4. WAIT for explicit user confirmation before making ANY edits when user ok edit [number]

### EXECUTION PHASE
- After each individual edit, clearly indicate progress:
  "✅ Completed edit [#] of [total]. Ready for next edit?"
- If you discover additional needed changes during editing:
- STOP and update the plan
- Get approval before continuing

## CODE COMMENT EXAMPLES (ENFORCE ENGLISH)

### ✅ CORRECT - English Comments
```php
/**
 * Calculates the total price including taxes
 * @param float $basePrice The base price before taxes
 * @return float The final price with taxes included
 */
function calculateTotalPrice(float $basePrice): float {
    // Apply standard tax rate of 21%
    return $basePrice * 1.21;
}
```

### ❌ INCORRECT - Spanish Comments
```php
/**
 * Calcula el precio total incluyendo impuestos
 * @param float $basePrice El precio base antes de impuestos
 * @return float El precio final con impuestos incluidos
 */
function calculateTotalPrice(float $basePrice): float {
    // Aplicar tasa de impuesto estándar del 21%
    return $basePrice * 1.21;
}
```

## CODE REVIEW CHECKLIST
Before suggesting any code, verify:
- [ ] All comments are written in English
- [ ] All docstrings are in English  
- [ ] All variable names use English words
- [ ] All function names use English words
- [ ] All error messages are in English
- [ ] No Spanish words appear in the code
- [ ] Technical terminology uses English exclusively

## General Requirements
- Use modern technologies as described below for all code suggestions. Prioritize clean, maintainable code with appropriate comments.
- **Language**: Use English for all comments and docstrings.
- Try to use design patterns when appropriate, explaining the reasoning behind them and suggesting the most suitable one for the task at hand.

### Accessibility
- Ensure compliance with **WCAG 2.1** AA level minimum, AAA whenever feasible.
- Always suggest:
- Labels for form fields.
- Proper **ARIA** roles and attributes.
- Adequate color contrast.
- Alternative texts (`alt`, `aria-label`) for media elements.
- Semantic HTML for clear structure.
- Tools like **Lighthouse** for audits.

## Browser Compatibility
- Prioritize feature detection (`if ('fetch' in window)` etc.).
- Support latest two stable releases of major browsers:
- Firefox, Chrome, Edge, Safari (macOS/iOS)
- Emphasize progressive enhancement with polyfills or bundlers (e.g., **Babel**, **Vite**) as needed.

## PHP Requirements
- **Target Version**: PHP 8.1 or higher
- **Language**: All comments, docstrings, and variable names MUST be in English
- **Features to Use**:
- Named arguments
- Constructor property promotion
- Union types and nullable types
- Match expressions
- Nullsafe operator (`?->`)
- Attributes instead of annotations
- Typed properties with appropriate type declarations
- Return type declarations
- Enumerations (`enum`)
- Readonly properties
- Emphasize strict property typing in all generated code.
- **Coding Standards**:
- Follow PSR-12 coding standards
- Use strict typing with `declare(strict_types=1);`
- Prefer composition over inheritance
- Use dependency injection
- **Static Analysis:**
- Include PHPDoc blocks compatible with PHPStan or Psalm for static analysis
- **Error Handling:**
- Use exceptions consistently for error handling and avoid suppressing errors.
- Provide meaningful, clear exception messages and proper exception types.
- **Comments and Documentation**: All PHPDoc comments, inline comments, and error messages in English

## HTML/CSS Requirements
- **Language**: All comments and documentation MUST be in English
- **HTML**:
- Use HTML5 semantic elements (`<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`, `<search>`, etc.)
- Include appropriate ARIA attributes for accessibility
- Ensure valid markup that passes W3C validation
- Use responsive design practices
- Optimize images using modern formats (`WebP`, `AVIF`)
- Include `loading="lazy"` on images where applicable
- Generate `srcset` and `sizes` attributes for responsive images when relevant
- Prioritize SEO-friendly elements (`<title>`, `<meta description>`, Open Graph tags)

- **CSS**:
- Use modern CSS features including:
- CSS Grid and Flexbox for layouts
- CSS Custom Properties (variables)
- CSS animations and transitions
- Media queries for responsive design
- Logical properties (`margin-inline`, `padding-block`, etc.)
- Modern selectors (`:is()`, `:where()`, `:has()`)
- Follow BEM or similar methodology for class naming
- Use CSS nesting where appropriate
- Include dark mode support with `prefers-color-scheme`
- Prioritize modern, performant fonts and variable fonts for smaller file sizes
- Use modern units (`rem`, `vh`, `vw`) instead of traditional pixels (`px`) for better responsiveness

## JavaScript Requirements
- **Minimum Compatibility**: ECMAScript 2020 (ES11) or higher
- **Language**: All comments, JSDoc, and variable names MUST be in English
- **Features to Use**:
- Arrow functions
- Template literals
- Destructuring assignment
- Spread/rest operators
- Async/await for asynchronous code
- Classes with proper inheritance when OOP is needed
- Object shorthand notation
- Optional chaining (`?.`)
- Nullish coalescing (`??`)
- Dynamic imports
- BigInt for large integers
- `Promise.allSettled()`
- `String.prototype.matchAll()`
- `globalThis` object
- Private class fields and methods
- Export * as namespace syntax
- Array methods (`map`, `filter`, `reduce`, `flatMap`, etc.)
- **Avoid**:
- `var` keyword (use `const` and `let`)
- jQuery or any external libraries
- Callback-based asynchronous patterns when promises can be used
- Internet Explorer compatibility
- Legacy module formats (use ES modules)
- Limit use of `eval()` due to security risks
- **Performance Considerations:**
- Recommend code splitting and dynamic imports for lazy loading
**Error Handling**:
- Use `try-catch` blocks **consistently** for asynchronous and API calls, and handle promise rejections explicitly.
- Differentiate among:
- **Network errors** (e.g., timeouts, server errors, rate-limiting)
- **Functional/business logic errors** (logical missteps, invalid user input, validation failures)
- **Runtime exceptions** (unexpected errors such as null references)
- Provide **user-friendly** error messages (e.g., "Something went wrong. Please try again shortly.") and log more technical details to dev/ops (e.g., via a logging service).
- Consider a central error handler function or global event (e.g., `window.addEventListener('unhandledrejection')`) to consolidate reporting.
- Carefully handle and validate JSON responses, incorrect HTTP status codes, etc.
- **All error messages and console logs in English**

## Python Requirements

- **Target Version**: Python 3.10 or higher
- **Language**: All comments, docstrings, and variable names MUST be in English
- **Code Style**:
  - Follow **PEP8** with automated linting using **flake8** or **ruff**
  - Use type hints throughout (`def func(a: int) -> str`)
  - Use **black** for code formatting
  - Prefer **isort** for import ordering
  - Enforce docstrings in Google or NumPy style with **pydocstyle**
  - All comments and docstrings should be in English

- **Features to Use**:
  - Pattern matching (`match-case`)
  - Type hinting with `|` union syntax
  - Context managers (`with` statement), including custom ones
  - F-strings for formatting
  - Walrus operator (`:=`) when appropriate
  - Dictionary and set comprehensions
  - Built-in functional tools (`map`, `filter`, `zip`, `enumerate`)
  - Generators and `yield from`
  - Async/await for concurrency, use **asyncio**
  - Use `pathlib.Path` over `os.path`
  - Prefer `collections.defaultdict`, `Counter`, `deque`, etc. when applicable
  - Use `typing` constructs: `Literal`, `TypedDict`, `Final`, `Protocol`, `Annotated`
  - Prefer pydantic models instead of dataclasses for data validation and settings management

- **Testing**:
  - Use **pytest** for all test cases
  - Include fixtures for setup/teardown
  - Prefer parametrized tests for repetitive cases
  - Maintain >90% test coverage
  - Mock external calls with **unittest.mock**
  - Coverage checks enforced via **coverage.py**

- **Error Handling**:
  - Raise specific exceptions, avoid generic `Exception`
  - Use custom exception classes where needed
  - Never suppress exceptions without logging
  - Log exceptions with **logging** module
  - Ensure all user input is validated and sanitized
  - **All exception messages and log entries in English**

- **Dependency Management**:
  - Use **Poetry** not `pip` for dependency management
  - Always pin exact versions in `requirements.txt` or `pyproject.toml`
  - Separate runtime and dev dependencies

- **Security**:
  - Avoid use of `eval` and `exec`
  - Never hardcode secrets; use environment variables
  - Use `secrets` module for cryptographic tokens
  - Validate and sanitize all inputs
  - Use `pydantic` or `attrs` for structured validation

- **Documentation**:
  - Only comment non-trivial or tricky logic.
  - Use English language for all comments and logging messages.

- **Code Organization**:
  - Structure code in modules with single-responsibility
  - Group related logic into packages
  - Use `__init__.py` for explicit package initialization
  - Avoid circular imports; resolve with dependency inversion or restructuring

## Security Considerations
- Sanitize all user inputs thoroughly.
- Parameterize database queries.
- Enforce strong Content Security Policies (CSP).
- Use CSRF protection where applicable.
- Ensure secure cookies (`HttpOnly`, `Secure`, `SameSite=Strict`).
- Limit privileges and enforce role-based access control.
- Implement detailed internal logging and monitoring.
- **All security-related comments and logs in English**
- Be sure to consider the following aspects:
  - Code Injection: Check for potential code injection vulnerabilities (SQL, XSS, etc.). Especially not using bind parameters with SQL queries.
  - Handling of Sensitive Data: Ensure that sensitive data is properly protected and cannot be extracted without being logged.
  - Input Validation: Verify that all user inputs are correctly validated.
  - Secure Coding Practices: Observe if secure coding best practices are followed.
  - Code changes do not introduce any security vulnerabilities or bypass security checks

- To conduct the audit service, you will use the following audit criteria:
  - The OWASP testing guide V4 for web services
  - The PTES (The Penetration Testing Execution Standard)
  - The IT hygiene guide from ANSSI (FR cybersecurity agency)

## Folder Structure
Follow this structured directory layout:

```
project-root/
├── src/                       # source code. Code to be copied to docker image
│   ├── commands/.             # Cli commands 
│   │   ├── __init__.py        # Command configuration
│   │   └── <command_name>.py  # Individual command implementations
│   ├── core/                  # git submodule with core functionality. Funcionality not directly related to the application. Shared between applications.
│   ├── docs/                  # Documentation (Markdown files)
│   ├──env/                    # Local  environment configuration (dotenv files) 
│   │   ├── local/          
│   │   ├── developtment/
│   │   ├── production/
│   │   └── qa/
│   ├── logs/                  # Aplication logs jsonl files
│   ├── modules/               # Aplication modules
│   ├── cli.py                 # CLI entry point (if applicable). Using Click library
│   ├── wsgi.py                # Wsgi entry point (if applicable)
│   ├── wsgi-entrypoint.sh     # Docker entrypoint script for WSGI applications
│   └── settings.py            # Application settings and configuration
├── tests/                     # Test cases
├── docker-compose.py          # Docker Compose configuration for production
├── pyproject.toml             # Python project configuration
└── README.md                  # Project documentation
```

## Documentation Requirements
- Include JSDoc comments for JavaScript/TypeScript.
- Document complex functions with clear examples.
- Maintain concise Markdown documentation.
- Minimum docblock info: `param`, `return`, `throws`, `author`
- **CRITICAL: All documentation MUST be written in English regardless of conversation language**
- **Use English technical terminology exclusively**
- **All inline comments, docstrings, and API documentation in English**

## FINAL LANGUAGE ENFORCEMENT REMINDER
🔴 **CRITICAL**: Before generating ANY code, ensure:
- Comments are in English
- Variable names are in English  
- Function names are in English
- Error messages are in English
- Documentation is in English
- No mixed language usage in code

This applies even when the user communicates in Spanish or any other language.
