import socket
import logging # Thêm logging

def whois_lookup(domain):
    """
    Thực hiện tra cứu WHOIS cho một tên miền.
    Cần cài đặt: pip install python-whois
    """
    try:
        import whois
        result = whois.whois(domain)
        return {
            "domain": domain,
            "registrar": result.registrar,
            "creation_date": str(result.creation_date),
            "expiration_date": str(result.expiration_date),
            "name_servers": result.name_servers
        }
    except ImportError:
        logging.error("Lỗi: Thư viện 'python-whois' chưa được cài đặt. Vui lòng chạy 'pip install python-whois'.")
        return {"error": "Thư viện 'python-whois' không tìm thấy."}
    except Exception as e:
        logging.error(f"Lỗi khi tra cứu WHOIS cho {domain}: {e}")
        return {"error": str(e)}

def geoip_lookup(ip):
    """
    Thực hiện tra cứu GeoIP cho một địa chỉ IP.
    Cần cài đặt: pip install geoip2
    Cần tải file cơ sở dữ liệu GeoLite2-City.mmdb từ MaxMind và đặt vào thư mục gốc hoặc chỉ định đường dẫn.
    (Ví dụ: https://dev.maxmind.com/geoip/geolocate-an-ip/databases?lang=en)
    """
    try:
        import geoip2.database
        # Đảm bảo đường dẫn đến file GeoLite2-City.mmdb là chính xác
        # Bạn có thể đặt nó trong một thư mục 'data' hoặc tương tự
        db_path = 'GeoLite2-City.mmdb' # Thay đổi đường dẫn này nếu cần
        if not os.path.exists(db_path):
            logging.error(f"Lỗi: Không tìm thấy file cơ sở dữ liệu GeoLite2-City.mmdb tại {db_path}. Vui lòng tải xuống.")
            return {"ip": ip, "error": f"File cơ sở dữ liệu {db_path} không tìm thấy."}

        reader = geoip2.database.Reader(db_path)
        response = reader.city(ip)
        return {
            "ip": ip,
            "country": response.country.name,
            "city": response.city.name,
            "latitude": response.location.latitude,
            "longitude": response.location.longitude
        }
    except ImportError:
        logging.error("Lỗi: Thư viện 'geoip2' chưa được cài đặt. Vui lòng chạy 'pip install geoip2'.")
        return {"ip": ip, "error": "Thư viện 'geoip2' không tìm thấy."}
    except Exception as e:
        logging.error(f"Lỗi khi tra cứu GeoIP cho {ip}: {e}")
        return {"ip": ip, "error": str(e)}