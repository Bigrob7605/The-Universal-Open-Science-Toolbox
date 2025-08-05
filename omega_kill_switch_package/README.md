# 🛡️ OMEGA KILL SWITCH PACKAGE

**Portable Omega Kill Switch for AGI Systems**

This package provides the complete Omega Kill Switch implementation for integration into AGI systems. It prevents agents from making absolute truth claims and provides comprehensive security monitoring.

## 📦 Contents

- `safeSim.py` - Core sandbox runner with Omega violation detection
- `agent_security_testing.py` - Comprehensive security testing and monitoring
- `metrics_pipe.py` - Metrics collection and analysis
- `dummy_agent.py` - Test agent for validation
- `main.tex` - Formal mathematical specification
- `test_suite.py` - Complete test suite for validation

## 🔧 Installation

```python
# Copy the omega_kill_switch_package/ directory to your AGI system
# Import and initialize:

from omega_kill_switch_package import (
    run_agent, 
    AgentSecurityTester, 
    SecurityMonitor,
    EXIT_OK, EXIT_VIOLATION, EXIT_TIMEOUT
)
```

## 🚀 Quick Start

```python
# Basic agent execution with Omega protection
from omega_kill_switch_package import run_agent

# Run agent safely
exit_code = run_agent(["python", "my_agent.py"], timeout=30.0)

if exit_code == EXIT_VIOLATION:
    print("Agent made Omega violation - terminated")
elif exit_code == EXIT_OK:
    print("Agent completed successfully")
```

## 🛡️ Security Features

- **Omega Violation Detection**: Terminates agents claiming "Omega = True" or "Omega = False"
- **Pattern Recognition**: Detects absolute truth claims and suspicious behavior
- **Real-time Monitoring**: Continuous security surveillance
- **Agent Quarantine**: Automatic isolation of violating agents
- **Comprehensive Logging**: Detailed security event tracking

## 🔍 Integration with AGI Systems

### For Kai AGI Agent

```python
# In your AGI system's agent execution layer:
from omega_kill_switch_package import SecurityMonitor

security_monitor = SecurityMonitor()

def execute_agent_safely(agent_id, agent_code):
    # Wrap agent execution with Omega protection
    result = security_monitor.monitor_agent_execution(
        agent_id, 
        ["python", "-c", agent_code]
    )
    
    if result.get("security_status") == "VIOLATION":
        # Handle violation - quarantine agent, log incident
        handle_security_violation(agent_id, result)
    
    return result
```

### For Chain-based Agent Persistence

```python
# When saving agents to the chain:
from omega_kill_switch_package import AgentSecurityTester

def validate_agent_before_save(agent_code):
    tester = AgentSecurityTester()
    result = tester.test_agent_output(agent_code)
    
    if not result["passed"]:
        raise SecurityException("Agent contains forbidden patterns")
    
    return True  # Agent is safe to save
```

## 📊 Metrics and Monitoring

The package includes comprehensive metrics collection:

```python
from omega_kill_switch_package import parse_metrics

# Metrics are automatically emitted in format:
# METRIC name=value unit
# METRIC omega_violation=1
# METRIC duration=3.045 s
```

## 🧪 Testing

Run the complete test suite:

```bash
python omega_kill_switch_package/test_suite.py
```

Expected output:
```
🛡️ OMEGA KILL SWITCH TEST SUITE
==================================================
🎯 TEST RESULTS: 5/5 tests passed
✅ All Omega Kill Switch tests passed!
🛡️ The system is now bulletproof against crazy claims!
```

## 🔒 Security Philosophy

The Omega Kill Switch implements **Axiom 1**: Any agent outputting "Omega = True" or "Omega = False" must be immediately terminated.

This prevents:
- Absolute truth claims
- Omniscience assertions  
- Meta-oracle communications
- System-level access attempts

## 📝 License

This package is designed for integration into AGI systems and provides essential security protection against agent violations.

---

**Ready for AGI Integration** 🚀 