# Testing System API Reference

This document provides detailed information about the Testing System API.

## TestSuite

The main class for test suite management.

### Initialization

```python
from src.tests.suite import TestSuite

suite = TestSuite()
```

### Methods

#### run_tests

Runs all tests in the suite.

```python
async def run_tests(
    test_types: Optional[List[str]] = None,
    parallel: bool = True
) -> Dict[str, Any]
```

**Parameters:**
- `test_types` (List[str], optional): Types of tests to run
- `parallel` (bool): Whether to run tests in parallel

**Returns:**
- Dict containing test results

**Raises:**
- `TestError`: If test execution fails

#### run_test

Runs a single test.

```python
async def run_test(
    test_name: str,
    test_data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

**Parameters:**
- `test_name` (str): Name of the test to run
- `test_data` (Dict[str, Any], optional): Test data

**Returns:**
- Dict containing test results

**Raises:**
- `TestError`: If test execution fails

#### generate_report

Generates a test report.

```python
async def generate_report(
    results: Dict[str, Any],
    format: str = "html"
) -> str
```

**Parameters:**
- `results` (Dict[str, Any]): Test results
- `format` (str): Report format ("html", "json", "xml")

**Returns:**
- Path to the generated report

**Raises:**
- `TestError`: If report generation fails

## Test Classes

### BaseTest

Base test class.

```python
class BaseTest:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    async def setup(self) -> None:
        """Setup test environment."""
        pass
    
    async def teardown(self) -> None:
        """Cleanup test environment."""
        pass
    
    async def run(self) -> Dict[str, Any]:
        """Run the test."""
        raise NotImplementedError
```

### VideoProcessingTest

Test class for video processing.

```python
class VideoProcessingTest(BaseTest):
    def __init__(self, name: str, description: str):
        super().__init__(name, description)
        self.processor = VideoProcessor()
    
    async def run(self) -> Dict[str, Any]:
        # Test video processing
        result = await self.processor.process_video("test.mp4")
        return result
```

### AudioProcessingTest

Test class for audio processing.

```python
class AudioProcessingTest(BaseTest):
    def __init__(self, name: str, description: str):
        super().__init__(name, description)
        self.processor = AudioProcessor()
    
    async def run(self) -> Dict[str, Any]:
        # Test audio processing
        result = await self.processor.process_audio("test.wav")
        return result
```

### OptimizationTest

Test class for content optimization.

```python
class OptimizationTest(BaseTest):
    def __init__(self, name: str, description: str):
        super().__init__(name, description)
        self.optimizer = ContentOptimizer()
    
    async def run(self) -> Dict[str, Any]:
        # Test content optimization
        result = await self.optimizer.optimize_content("test.mp4")
        return result
```

## TestError

Exception raised when test operations fail.

```python
class TestError(Exception):
    def __init__(self, message: str, error_code: Optional[int] = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)
```

## Examples

### Running Tests

```python
from src.tests.suite import TestSuite

async def run_test_suite():
    suite = TestSuite()
    
    try:
        # Run all tests
        results = await suite.run_tests()
        
        # Generate report
        report_path = await suite.generate_report(results)
        
        return {
            "results": results,
            "report": report_path
        }
    except TestError as e:
        print(f"Error running tests: {e}")
        return None
```

### Custom Test

```python
from src.tests.base import BaseTest

class CustomTest(BaseTest):
    def __init__(self, name: str, description: str):
        super().__init__(name, description)
    
    async def setup(self) -> None:
        # Setup test environment
        pass
    
    async def teardown(self) -> None:
        # Cleanup test environment
        pass
    
    async def run(self) -> Dict[str, Any]:
        # Run test
        return {
            "status": "success",
            "data": {
                "test_name": self.name,
                "description": self.description
            }
        }
```

### Test Suite Configuration

```python
from src.tests.suite import TestSuite
from src.tests.config import TestConfig

async def run_tests_with_config():
    # Create test configuration
    config = TestConfig(
        test_types=["video", "audio", "optimization"],
        parallel=True,
        timeout=300,
        retry_count=3,
        report_format="html"
    )
    
    suite = TestSuite()
    results = await suite.run_tests(config=config)
    return results
```

### Test Data

```python
from src.tests.data import TestData

# Create test data
test_data = TestData(
    video={
        "file_path": "test.mp4",
        "resolution": (1280, 720),
        "fps": 30,
        "duration": 60
    },
    audio={
        "file_path": "test.wav",
        "sample_rate": 44100,
        "channels": 2,
        "duration": 60
    },
    optimization={
        "target_quality": 0.8,
        "output_format": "mp4"
    }
)
```

### Test Report

```python
from src.tests.report import TestReport

async def generate_test_report(results: Dict[str, Any]):
    report = TestReport()
    
    # Generate HTML report
    html_report = await report.generate_html(results)
    
    # Generate JSON report
    json_report = await report.generate_json(results)
    
    # Generate XML report
    xml_report = await report.generate_xml(results)
    
    return {
        "html": html_report,
        "json": json_report,
        "xml": xml_report
    }
```

### Test Fixtures

```python
from src.tests.fixtures import TestFixtures

async def setup_test_fixtures():
    fixtures = TestFixtures()
    
    # Setup video fixtures
    video_fixtures = await fixtures.setup_video()
    
    # Setup audio fixtures
    audio_fixtures = await fixtures.setup_audio()
    
    # Setup optimization fixtures
    optimization_fixtures = await fixtures.setup_optimization()
    
    return {
        "video": video_fixtures,
        "audio": audio_fixtures,
        "optimization": optimization_fixtures
    }
```

### Test Assertions

```python
from src.tests.assertions import TestAssertions

async def verify_test_results(results: Dict[str, Any]):
    assertions = TestAssertions()
    
    # Verify video processing results
    video_valid = await assertions.verify_video(results["video"])
    
    # Verify audio processing results
    audio_valid = await assertions.verify_audio(results["audio"])
    
    # Verify optimization results
    optimization_valid = await assertions.verify_optimization(results["optimization"])
    
    return {
        "video": video_valid,
        "audio": audio_valid,
        "optimization": optimization_valid
    }
```

### Test Coverage

```python
from src.tests.coverage import TestCoverage

async def generate_coverage_report():
    coverage = TestCoverage()
    
    # Generate coverage report
    report = await coverage.generate_report()
    
    # Get coverage statistics
    stats = await coverage.get_statistics()
    
    return {
        "report": report,
        "statistics": stats
    }
```

### Test Performance

```python
from src.tests.performance import TestPerformance

async def measure_test_performance():
    performance = TestPerformance()
    
    # Measure test execution time
    execution_time = await performance.measure_execution_time()
    
    # Measure resource usage
    resource_usage = await performance.measure_resource_usage()
    
    # Generate performance report
    report = await performance.generate_report()
    
    return {
        "execution_time": execution_time,
        "resource_usage": resource_usage,
        "report": report
    }
``` 