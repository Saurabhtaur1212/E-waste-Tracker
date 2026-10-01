-- GreenTrace logical database schema
CREATE TABLE users(
 id SERIAL PRIMARY KEY,
 name VARCHAR(120) NOT NULL,
 email VARCHAR(200) UNIQUE NOT NULL,
 role VARCHAR(40) DEFAULT 'student',
 department VARCHAR(120),
 green_credits INTEGER DEFAULT 0
);

CREATE TABLE ewaste_assets(
 id SERIAL PRIMARY KEY,
 asset_id VARCHAR(100) UNIQUE NOT NULL,
 device_type VARCHAR(100) NOT NULL,
 serial_number VARCHAR(150),
 institution VARCHAR(180),
 department VARCHAR(120),
 condition VARCHAR(100),
 status VARCHAR(80),
 recycler VARCHAR(200),
 recycler_verified BOOLEAN DEFAULT FALSE,
 certificate_id VARCHAR(150),
 updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE ewaste_lifecycle(
 id SERIAL PRIMARY KEY,
 asset_id VARCHAR(100) NOT NULL,
 previous_status VARCHAR(80),
 new_status VARCHAR(80) NOT NULL,
 actor VARCHAR(150),
 location VARCHAR(200),
 remarks TEXT,
 timestamp TIMESTAMP DEFAULT NOW()
);

CREATE TABLE smart_bins(
 id SERIAL PRIMARY KEY,
 bin_id VARCHAR(100) UNIQUE NOT NULL,
 location VARCHAR(200),
 waste_type VARCHAR(80),
 fill_level NUMERIC,
 temperature NUMERIC,
 battery NUMERIC,
 status VARCHAR(60),
 updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE green_credits(
 id SERIAL PRIMARY KEY,
 user_id INTEGER,
 action VARCHAR(180),
 points INTEGER,
 verified BOOLEAN DEFAULT TRUE,
 reference VARCHAR(180),
 created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE audit_logs(
 id SERIAL PRIMARY KEY,
 actor VARCHAR(200),
 action VARCHAR(250),
 reference VARCHAR(200),
 created_at TIMESTAMP DEFAULT NOW()
);
