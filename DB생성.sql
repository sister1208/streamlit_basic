CREATE DATABASE dashboard_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE dashboard_db;

CREATE TABLE sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_date DATE NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    region VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    -- 조회 성능 개선용 인덱스
    -- INDEX idx_sales_category_region_id (category, region, id),
    -- INDEX idx_sales_order_date (order_date)
);

INSERT INTO sales (order_date, product_name, category, quantity, price, region)
VALUES
('2026-03-01', '노트북', '전자', 3, 1200000, '서울'),
('2026-03-02', '마우스', '전자', 10, 25000, '부산'),
('2026-03-03', '의자', '가구', 5, 80000, '서울'),
('2026-03-04', '책상', '가구', 2, 150000, '대전'),
('2026-03-05', '키보드', '전자', 7, 70000, '인천');


-- 데이터베이스 선택
USE dashboard_db;

-- 고객 테이블 생성
CREATE TABLE IF NOT EXISTS customers (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    region VARCHAR(20) NOT NULL,
    age TINYINT UNSIGNED NOT NULL,
    join_date DATE NOT NULL,
    sales DECIMAL(12, 2) NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- 데이터 유효성 검사(MySQL 8.0.16 이상)
    CONSTRAINT chk_customers_age
        CHECK (age BETWEEN 1 AND 120),

    CONSTRAINT chk_customers_sales
        CHECK (sales >= 0),

    -- 조회 성능 개선용 인덱스
    INDEX idx_customers_region_id (region, id),
    INDEX idx_customers_join_date (join_date),
    INDEX idx_customers_name (name)
)



-- 샘플 데이터 입력
INSERT INTO customers
    (name, region, age, join_date, sales)
VALUES
    ('김민준', '서울', 29, '2025-01-10', 1250000.00),
    ('이서연', '부산', 34, '2025-01-18', 980000.00),
    ('박지훈', '대구', 41, '2025-02-03', 2150000.00),
    ('최유진', '인천', 27, '2025-02-15', 760000.00),
    ('정현우', '광주', 38, '2025-03-01', 1840000.00),
    ('강수빈', '대전', 32, '2025-03-12', 1320000.00),
    ('조하준', '서울', 45, '2025-03-25', 3150000.00),
    ('윤지아', '부산', 24, '2025-04-07', 540000.00),
    ('장도윤', '대구', 36, '2025-04-19', 1680000.00),
    ('임채원', '인천', 30, '2025-05-02', 1120000.00),
    ('한서준', '광주', 52, '2025-05-15', 4280000.00),
    ('오민서', '대전', 28, '2025-05-28', 890000.00),
    ('서예준', '서울', 39, '2025-06-09', 2450000.00),
    ('신지우', '부산', 33, '2025-06-21', 1470000.00),
    ('권시우', '대구', 47, '2025-07-04', 3560000.00),
    ('황나연', '인천', 26, '2025-07-17', 680000.00),
    ('안준호', '광주', 43, '2025-08-01', 2780000.00),
    ('송다은', '대전', 31, '2025-08-14', 1180000.00),
    ('전우진', '서울', 55, '2025-09-03', 5120000.00),
    ('홍서아', '부산', 22, '2025-09-20', 430000.00);


-- 생성 결과 확인
SELECT
    id,
    name,
    region,
    age,
    join_date,
    sales,
    created_at
FROM customers
ORDER BY id DESC;

USE dashboard_db;

-- 조회 성능 개선용 인덱스 생성
CREATE INDEX idx_sales_category_region_id ON sales(category, region, id);
CREATE INDEX idx_sales_order_date ON sales(order_date);
CREATE INDEX idx_customers_region_id ON customers(region, id);
CREATE INDEX idx_customers_join_date ON customers(join_date);
CREATE INDEX idx_customers_name ON customers(name);


-- 주문 테이블 생성 및 데이터 삽입

CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_date DATE NOT NULL,
    customer_name VARCHAR(50) NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    region VARCHAR(50) NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(12,2) NOT NULL,
    discount_rate DECIMAL(5,2) NOT NULL DEFAULT 0,
    payment_method VARCHAR(30) NOT NULL,
    order_status VARCHAR(30) NOT NULL DEFAULT '주문 접수',
    urgent_order BOOLEAN NOT NULL DEFAULT FALSE,
    receive_message BOOLEAN NOT NULL DEFAULT TRUE,
    memo VARCHAR(500),
    attachment_name VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_orders_date (order_date),
    INDEX idx_orders_category_region (category, region),
    INDEX idx_orders_status (order_status),
    INDEX idx_orders_customer (customer_name),
    INDEX idx_orders_product (product_name)
);

INSERT INTO orders (
    order_date,
    customer_name,
    product_name,
    category,
    region,
    quantity,
    unit_price,
    discount_rate,
    payment_method,
    order_status,
    urgent_order,
    receive_message,
    memo,
    attachment_name
)
VALUES
-- 전자기기
('2026-08-01', '김민수', '노트북', '전자기기', '서울',
 2, 1200000, 5, '카드', '배송 완료', FALSE, TRUE,
 '오전 배송 요청', NULL),

('2026-08-03', '이서연', '모니터', '전자기기', '부산',
 3, 350000, 10, '계좌이체', '배송 완료', FALSE, TRUE,
 '회사 사무실로 배송', 'purchase_order_1002.pdf'),

('2026-08-05', '박지훈', '키보드', '전자기기', '대구',
 5, 80000, 0, '카드', '배송 완료', FALSE, FALSE,
 NULL, NULL),

('2026-08-07', '최유리', '노트북', '전자기기', '서울',
 1, 1200000, 3, '카드', '배송 중', TRUE, TRUE,
 '긴급 배송 요청', NULL),

('2026-08-09', '정하늘', '모니터', '전자기기', '인천',
 2, 350000, 5, '현금', '배송 완료', FALSE, TRUE,
 NULL, 'monitor_order.xlsx'),

('2026-08-11', '한지민', '키보드', '전자기기', '부산',
 10, 80000, 8, '계좌이체', '배송 완료', FALSE, TRUE,
 '교육장 비품', NULL),

('2026-08-13', '오세훈', '노트북', '전자기기', '광주',
 4, 1200000, 12, '후불 결제', '주문 접수', TRUE, TRUE,
 '법인 대량 구매', 'company_order.pdf'),

('2026-08-15', '서은우', '모니터', '전자기기', '대전',
 6, 350000, 7, '카드', '배송 중', FALSE, TRUE,
 '모니터 암과 함께 배송', NULL),

('2026-08-17', '윤도현', '키보드', '전자기기', '서울',
 3, 80000, 0, '현금', '주문 취소', FALSE, FALSE,
 '고객 요청으로 취소', NULL),

('2026-08-19', '강수진', '노트북', '전자기기', '인천',
 2, 1200000, 5, '계좌이체', '배송 완료', TRUE, TRUE,
 '보안실 경유 배송', NULL),

-- 가구
('2026-08-21', '김영희', '사무용 의자', '가구', '서울',
 5, 180000, 5, '카드', '배송 완료', FALSE, TRUE,
 '조립 후 배송 요청', NULL),

('2026-08-23', '이준호', '책상', '가구', '부산',
 2, 250000, 0, '계좌이체', '배송 완료', FALSE, TRUE,
 '엘리베이터 없는 3층', NULL),

('2026-08-25', '박서연', '사무용 의자', '가구', '대구',
 8, 180000, 10, '후불 결제', '배송 중', TRUE, TRUE,
 '회의실 비품', 'furniture_order.xlsx'),

('2026-08-27', '최민준', '책상', '가구', '인천',
 4, 250000, 5, '카드', '주문 접수', FALSE, TRUE,
 NULL, NULL),

('2026-08-29', '정유진', '사무용 의자', '가구', '광주',
 2, 180000, 0, '현금', '배송 완료', FALSE, FALSE,
 '경비실에 맡겨주세요', NULL),

('2026-09-01', '한서준', '책상', '가구', '대전',
 10, 250000, 15, '계좌이체', '배송 중', TRUE, TRUE,
 '교육장 책상 교체', 'desk_order.pdf'),

('2026-09-03', '오지민', '사무용 의자', '가구', '서울',
 3, 180000, 3, '카드', '배송 완료', FALSE, TRUE,
 NULL, NULL),

('2026-09-05', '서도윤', '책상', '가구', '부산',
 1, 250000, 0, '현금', '주문 취소', FALSE, FALSE,
 '배송 일정 불일치로 취소', NULL),

('2026-09-07', '윤하은', '사무용 의자', '가구', '대구',
 6, 180000, 7, '후불 결제', '주문 접수', FALSE, TRUE,
 '법인 주문', NULL),

('2026-09-09', '강현우', '책상', '가구', '인천',
 3, 250000, 5, '카드', '배송 중', TRUE, TRUE,
 '이번 주 내 배송 요청', NULL),

-- 사무용품
('2026-09-10', '김서현', '복사용지', '사무용품', '서울',
 20, 30000, 5, '계좌이체', '배송 완료', FALSE, TRUE,
 'A4 용지', NULL),

('2026-09-11', '이도현', '복사용지', '사무용품', '부산',
 15, 30000, 0, '카드', '배송 완료', FALSE, FALSE,
 NULL, NULL),

('2026-09-12', '박하윤', '복사용지', '사무용품', '대구',
 30, 30000, 10, '후불 결제', '배송 중', TRUE, TRUE,
 '교육과정 실습용', 'paper_order.xlsx'),

('2026-09-13', '최지우', '복사용지', '사무용품', '인천',
 10, 30000, 0, '현금', '주문 접수', FALSE, TRUE,
 NULL, NULL),

('2026-09-14', '정민재', '복사용지', '사무용품', '광주',
 25, 30000, 8, '계좌이체', '배송 완료', FALSE, TRUE,
 '매월 정기 주문', NULL),

-- 추가 혼합 데이터
('2026-09-15', '한수아', '노트북', '전자기기', '대전',
 3, 1200000, 10, '카드', '주문 접수', TRUE, TRUE,
 '신규 입사자 지급용', 'laptop_order.pdf'),

('2026-09-15', '오민석', '모니터', '전자기기', '서울',
 5, 350000, 5, '후불 결제', '배송 중', FALSE, TRUE,
 '듀얼 모니터 구성', NULL),

('2026-09-16', '서예진', '사무용 의자', '가구', '부산',
 4, 180000, 0, '계좌이체', '주문 접수', FALSE, TRUE,
 '색상은 검정으로 요청', NULL),

('2026-09-16', '윤성호', '책상', '가구', '대구',
 7, 250000, 12, '카드', '배송 중', TRUE, TRUE,
 '조립 서비스 포함', 'desk_layout.png'),

('2026-09-16', '강지민', '키보드', '전자기기', '서울',
 12, 80000, 10, '계좌이체', '주문 접수', FALSE, TRUE,
 '개발팀 장비 교체', 'keyboard_order.csv');