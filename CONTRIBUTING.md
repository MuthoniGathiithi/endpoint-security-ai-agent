# Contributing to Endpoint Security AI Agent

Thank you for your interest in contributing to the Endpoint Security AI Agent project! We're excited to have you on board. This guide will help you get started with setting up the development environment and making your first contribution.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Fork and Clone](#fork-and-clone)
  - [Environment Setup](#environment-setup)
- [Development Workflow](#development-workflow)
  - [Running the Backend](#running-the-backend)
  - [Running the Frontend](#running-the-frontend)
  - [Running Tests](#running-tests)
  - [Code Style](#code-style)
- [Making Changes](#making-changes)
- [Submitting a Pull Request](#submitting-a-pull-request)
- [Reporting Issues](#reporting-issues)
- [License](#license)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/) (v20.10.0+)
- [Docker Compose](https://docs.docker.com/compose/) (v2.0.0+)
- [Node.js](https://nodejs.org/) (v18.0.0+)
- [Python](https://www.python.org/) (v3.9+)
- [Git](https://git-scm.com/)

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your forked repository:
   ```bash
   git clone https://github.com/your-username/endpoint-security-ai-agent.git
   cd endpoint-security-ai-agent
   ```
3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/original-owner/endpoint-security-ai-agent.git
   ```

### Environment Setup

1. Create a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install Node.js dependencies:
   ```bash
   cd dashboard
   npm install
   cd ..
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file with your configuration.

## Development Workflow

### Running the Backend

```bash
# Start the FastAPI backend with hot-reload
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000` and the interactive API documentation at `http://localhost:8000/api/docs`.

### Running the Frontend

```bash
# Navigate to the dashboard directory
cd dashboard

# Start the Next.js development server
npm run dev
```

The frontend will be available at `http://localhost:3000`.

### Running with Docker

To run the entire stack with Docker Compose:

```bash
docker compose up --build
```

This will start:
- Backend API on port 8000
- Frontend on port 3000
- Redis on port 6379

### Running Tests

```bash
# Run Python tests
pytest

# Run frontend tests
cd dashboard
npm test
```

### Code Style

We use:
- **Python**: Black for formatting, isort for import sorting, and flake8 for linting
- **TypeScript/JavaScript**: Prettier for formatting and ESLint for linting

Format your code before committing:

```bash
# Format Python code
black .
isort .

# Format frontend code
cd dashboard
npm run format
```

## Making Changes

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-number-description
   ```

2. Make your changes and ensure tests pass.

3. Commit your changes with a descriptive commit message:
   ```bash
   git commit -m "feat: add new feature"
   # or
   git commit -m "fix: resolve issue with X"
   ```

4. Push your changes to your fork:
   ```bash
   git push origin your-branch-name
   ```

## Submitting a Pull Request

1. Go to the original repository and click on "New Pull Request".
2. Select your fork and branch to create the PR.
3. Fill in the PR template with details about your changes.
4. Ensure all tests pass and your code is properly formatted.
5. Request a review from one of the maintainers.

## Reporting Issues

If you find a bug or have a feature request, please open an issue on GitHub. When reporting a bug, please include:

- A clear description of the issue
- Steps to reproduce the problem
- Expected vs. actual behavior
- Screenshots if applicable
- Your environment details (OS, browser, etc.)

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
