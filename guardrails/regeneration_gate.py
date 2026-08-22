class RegenerationGate:
    
    MAX_RETRIES = 2
    
    def should_retry(self, guardrail_result, retry_count):
        
        if guardrail_result.passed:
            return False
        
        return retry_count < self.MAX_RETRIES