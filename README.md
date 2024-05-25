# E-commerce website

## Thành viên
- Nguyễn Hoàng Vũ (22022502)
- Triệu Vũ Hoàn (22022654)

License: MIT

## Cách chạy dự án

- Yêu cầu: Docker và Docker Compose
- Chạy lệnh sau để build các image.

      $ docker compose build

  câu lệch này chạy lần đầu có thể tốn nhiều thời gian tuy nhiên chỉ chạy 1 lần duy nhất.

- Tiếp theo khởi chạy các container câu lệch nay được chạy mỗi khi cần chạy ứng dụng.

      $ docker compose up -d

- Để dừng các container

      $ docker compose stop

- Khởi tạo dữ liệu cho trang web : lệnh này cũng chỉ chạy 1 lần hoặc khi có sự thay đổi nào liên quan đến dữ liệu.

      $ docker compose run --rm django python manage.py \ loaddata categories.json subcategories.json \
      fashions.json movies.json users2.json reviews2.json

- Mở trình duyệt và truy cập vào địa chỉ  http://127.0.0.1:8000/ hoặc http://127.0.0.1:8000/admin để truy cập vào trang admin.
