"""
Omega Kill Switch Package for AGI Systems

This package provides comprehensive security protection against agents making absolute truth claims.
Designed for integration into AGI systems with 24/7 operation capabilities.

Core Components:
- safeSim: Core sandbox runner with Omega violation detection
- AgentSecurityTester: Comprehensive security testing and monitoring
- SecurityMonitor: Real-time security monitoring and agent quarantine
- Metrics collection and analysis
- Complete test suite for validation
"""

# Core Omega Kill Switch components
from .safeSim import run_agent, EXIT_OK, EXIT_VIOLATION, EXIT_TIMEOUT, EXIT_INTERNAL
from .agent_security_testing import AgentSecurityTester, SecurityMonitor, security_monitor
from .metrics_pipe import parse_metrics, ensure_db, insert_db, append_csv

# Version and package info
__version__ = "2.0.0"
__author__ = "Universal Open Science Toolbox"
__description__ = "Omega Kill Switch for AGI Systems"

# Main exports for AGI integration
__all__ = [
    # Core execution
    "run_agent",
    "EXIT_OK", 
    "EXIT_VIOLATION", 
    "EXIT_TIMEOUT", 
    "EXIT_INTERNAL",
    
    # Security testing
    "AgentSecurityTester",
    "SecurityMonitor", 
    "security_monitor",
    
    # Metrics
    "parse_metrics",
    "ensure_db",
    "insert_db", 
    "append_csv",
    
    # Package info
    "__version__",
    "__author__",
    "__description__"
]

# Quick setup function for AGI systems
def setup_omega_protection():
    """
    Quick setup function for AGI systems.
    
    Returns:
        SecurityMonitor: Configured security monitor instance
    """
    monitor = SecurityMonitor()
    print("🛡️ Omega Kill Switch initialized for AGI protection")
    print("✅ Ready to monitor agents and prevent absolute truth claims")
    return monitor

# Validation function for agent code
def validate_agent_code(agent_code: str) -> dict:
    """
    Validate agent code for Omega violations before execution.
    
    Args:
        agent_code: The agent code to validate
        
    Returns:
        dict: Validation results with security status
    """
    tester = AgentSecurityTester()
    return tester.test_agent_output(agent_code)

# AGI integration helper
def execute_agent_safely(agent_id: str, agent_command: list, timeout: float = 30.0) -> dict:
    """
    Execute an agent with full Omega Kill Switch protection.
    
    Args:
        agent_id: Unique identifier for the agent
        agent_command: Command to execute
        timeout: Maximum execution time in seconds
        
    Returns:
        dict: Execution results with security status
    """
    monitor = SecurityMonitor()
    return monitor.monitor_agent_execution(agent_id, agent_command)

# Chain persistence helper
def validate_agent_for_persistence(agent_code: str) -> bool:
    """
    Validate agent code before saving to chain.
    
    Args:
        agent_code: The agent code to validate
        
    Returns:
        bool: True if agent is safe to persist
    """
    result = validate_agent_code(agent_code)
    return result["passed"]

print(f"Omega Kill Switch Package v{__version__} loaded")
print("Ready for AGI system integration") 