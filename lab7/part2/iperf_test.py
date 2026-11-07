from parser import parse_iperf

class TestSuite:
    def test_iperf3_client_connection(self, client):
        out, err = client
        print(" > Received from fixture client is:\n{}".format(out)) 
        assert not err

        parsed_data = parse_iperf(out)

        for item in parsed_data:
            assert item['Transfer'] > 2.0
            assert item['Bitrate'] > 31.0
