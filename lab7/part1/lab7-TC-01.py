import subprocess
import re

def client(server_ip):
    """Connects to the iperf server and returns standard output and error stream."""
    try:
        command = ["iperf", "-c", server_ip, "-i", "1"]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        out, err = process.communicate(timeout=15)
        return out, err
    except Exception as e:
        return "", str(e)

def parser(output_text):
    """Parses iperf output and returns a list of dictionaries with interval details."""
    results = []
    pattern = r"(\d+\.\d+-\d+\.\d+)\s+sec\s+(\d+\.?\d*)\s+[KMG]Bytes\s+(\d+\.?\d*)\s+[KMG]bits/sec"
    matches = re.findall(pattern, output_text)
    
    for match in matches:
        results.append({
            'Interval': match[0],
            'Transfer': float(match[1]),
            'Bitrate': float(match[2])
        })
    return results

def test_bandwidth_stability(server_ip):
    """Main automated test function to evaluate bandwidth stability."""
   
    result, error = client(server_ip)
    
    # Check 1: Connection errors
    if error or "Connection refused" in result:
        print(f"[-] FAILED: Connection error ({error or 'Connection refused'})")
        return

    parsed_data = parser(result)
    
    # Check 2: Insufficient data for analysis
    if len(parsed_data) < 2:
        print("[-] FAILED: Insufficient data for analysis.")
        return

    # Filter out summary rows (which span more than 1 second, since we use -i 1)
    # We calculate (end - start) from the interval string. If it's > 1.5, it's a summary row.
    interval_data = [
        item for item in parsed_data 
        if float(item['Interval'].split('-')[1]) - float(item['Interval'].split('-')[0]) <= 1.5
    ]
    
    # Check if there is data left after filtering
    if not interval_data:
        print("[-] FAILED: No valid interval data found after filtering.")
        return

    # Calculate average bitrate and stability threshold (70% of average)
    bitrates = [item['Bitrate'] for item in interval_data]
    avg_bitrate = sum(bitrates) / len(bitrates)
    threshold = avg_bitrate * 0.7 
    
    is_stable = True
    
    # Check 3: Bandwidth drops below threshold
    for item in interval_data:
        if item['Bitrate'] < threshold:
            print(f"[-] FAILED: Anomaly at interval {item['Interval']} sec. Bitrate {item['Bitrate']} dropped below threshold {threshold:.2f} (Average: {avg_bitrate:.2f}).")
            is_stable = False
            
    if is_stable:
        print(f"[+] PASSED: Connection is stable. Average bitrate: {avg_bitrate:.2f} Mbits/sec, no drops below 30% detected.")

server_ip = "127.0.0.1"
if __name__ == "__main__":
    test_bandwidth_stability(server_ip)
