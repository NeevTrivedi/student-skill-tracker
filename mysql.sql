CREATE DATABASE IF NOT EXISTS skill_tracker_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE skill_tracker_db;

-- 1. Student Profile Extension Table
CREATE TABLE tracker_studentprofile (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    college VARCHAR(255) NOT NULL DEFAULT '',
    course VARCHAR(150) NOT NULL DEFAULT '',
    year_of_study VARCHAR(20) NOT NULL DEFAULT '1st Year',
    bio TEXT NULL,
    created_at DATETIME(6) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE
);

-- 2. Skills Table
CREATE TABLE tracker_skill (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    proficiency VARCHAR(20) NOT NULL DEFAULT 'Beginner',
    progress_percentage INT NOT NULL DEFAULT 0,
    start_date DATE NOT NULL,
    target_date DATE NOT NULL,
    notes TEXT NULL,
    created_at DATETIME(6) NOT NULL,
    updated_at DATETIME(6) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE
);

-- 3. Learning Goals Table
CREATE TABLE tracker_learninggoal (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    goal_type VARCHAR(20) NOT NULL DEFAULT 'Weekly',
    target_date DATE NOT NULL,
    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at DATETIME(6) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE
);

-- 4. Activity Logs for Timeline
CREATE TABLE tracker_activitylog (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    action_text VARCHAR(255) NOT NULL,
    created_at DATETIME(6) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE
);