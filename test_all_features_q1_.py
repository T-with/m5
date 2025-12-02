"""
Free Recruitment Market - Complete Test Suite
Test all API endpoints and features
"""

import requests
import json
import time
from typing import Dict, Any
from datetime import datetime

# API Base URL
API_BASE = 'http://127.0.0.1:8000'

# Color output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_success(message: str):
    print(f"{Colors.GREEN}✓ {message}{Colors.RESET}")

def print_error(message: str):
    print(f"{Colors.RED}✗ {message}{Colors.RESET}")

def print_info(message: str):
    print(f"{Colors.CYAN}ℹ {message}{Colors.RESET}")

def print_section(message: str):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{message}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")

# Global variables to store test data
test_data = {
    'freelancer_ids': [],
    'evaluator_ids': [],
    'rating_ids': []
}

def test_health_check():
    """Test 1: Health Check"""
    print_section("Test 1: Health Check")
    
    try:
        response = requests.get(f'{API_BASE}/api/health', timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"API health check passed")
            print_info(f"  - Status: {data.get('status')}")
            print_info(f"  - Service: {data.get('service')}")
            print_info(f"  - Version: {data.get('version')}")
            print_info(f"  - Timestamp: {data.get('timestamp')}")
            return True
        else:
            print_error(f"Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Health check exception: {str(e)}")
        return False

def test_root_endpoint():
    """Test 2: Root Endpoint"""
    print_section("Test 2: Root Endpoint")
    
    try:
        response = requests.get(f'{API_BASE}/', timeout=5)
        
        if response.status_code == 200:
            # Root endpoint may return HTML or JSON
            content_type = response.headers.get('content-type', '')
            
            if 'application/json' in content_type:
                data = response.json()
                print_success("Root endpoint accessed successfully (JSON)")
                print_info(f"  - Message: {data.get('message')}")
                print_info(f"  - Version: {data.get('version')}")
            elif 'text/html' in content_type:
                print_success("Root endpoint accessed successfully (HTML home page)")
                print_info(f"  - Content type: HTML")
                print_info(f"  - Page size: {len(response.content)} bytes")
            else:
                print_success(f"Root endpoint accessed successfully")
                print_info(f"  - Content type: {content_type}")
            
            return True
        else:
            print_error(f"Root endpoint access failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Root endpoint access exception: {str(e)}")
        return False

def test_create_freelancers():
    """Test 3: Create Freelancers"""
    print_section("Test 3: Create Freelancers")
    
    freelancers = [
        {
            'name': 'John Smith',
            'email': 'john.smith@example.com',
            'phone': '+1-555-0101',
            'location': 'New York, NY',
            'job_type': 'Python Backend Engineer',
            'skills': 'Python, FastAPI, PostgreSQL, Docker',
            'about_me': '5 years backend development experience, specialized in microservices',
            'work_experience': 'Previously worked at a major tech company, responsible for core business systems',
            'availability': 'available'
        },
        {
            'name': 'Sarah Johnson',
            'email': 'sarah.j@example.com',
            'phone': '+1-555-0102',
            'location': 'San Francisco, CA',
            'job_type': 'Frontend Engineer',
            'skills': 'React, Vue, TypeScript, Tailwind CSS',
            'about_me': '3 years frontend development experience, focus on user experience',
            'work_experience': 'Participated in frontend architecture design for multiple large projects',
            'availability': 'available'
        },
        {
            'name': 'Michael Chen',
            'email': 'michael.chen@example.com',
            'phone': '+1-555-0103',
            'location': 'Seattle, WA',
            'job_type': 'Full Stack Engineer',
            'skills': 'Node.js, React, MongoDB, AWS',
            'about_me': '7 years full stack development experience, familiar with cloud-native architecture',
            'work_experience': 'Tech lead at startup, led team to complete multiple projects',
            'availability': 'busy'
        }
    ]
    
    success_count = 0
    for freelancer in freelancers:
        try:
            response = requests.post(
                f'{API_BASE}/api/freelancers',
                json=freelancer,
                timeout=5
            )
            
            if response.status_code == 201:
                data = response.json()
                freelancer_id = data.get('freelancer_id')
                test_data['freelancer_ids'].append(freelancer_id)
                print_success(f"Created freelancer: {freelancer['name']} (ID: {freelancer_id})")
                success_count += 1
            else:
                print_error(f"Failed to create freelancer: {freelancer['name']} - {response.text}")
        except Exception as e:
            print_error(f"Exception creating freelancer: {freelancer['name']} - {str(e)}")
    
    print_info(f"\nSuccessfully created {success_count}/{len(freelancers)} freelancers")
    return success_count > 0

def test_list_freelancers():
    """Test 4: List Freelancers"""
    print_section("Test 4: List Freelancers")
    
    try:
        response = requests.get(f'{API_BASE}/api/freelancers', timeout=5)
        
        if response.status_code == 200:
            freelancers = response.json()
            print_success(f"Retrieved freelancer list successfully, total: {len(freelancers)}")
            
            for freelancer in freelancers[:3]:  # Show first 3
                print_info(f"\n  Freelancer: {freelancer['name']}")
                print_info(f"    - ID: {freelancer['id']}")
                print_info(f"    - Email: {freelancer['email']}")
                print_info(f"    - Job Type: {freelancer.get('job_type', 'N/A')}")
                print_info(f"    - Location: {freelancer.get('location', 'N/A')}")
                print_info(f"    - Status: {freelancer['availability']}")
                
                rating_info = freelancer.get('rating_info', {})
                print_info(f"    - Average Rating: {rating_info.get('average', 0):.1f}")
                print_info(f"    - Review Count: {rating_info.get('total_reviews', 0)}")
            
            return True
        else:
            print_error(f"Failed to retrieve freelancer list: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Exception retrieving freelancer list: {str(e)}")
        return False

def test_get_freelancer_detail():
    """Test 5: Get Freelancer Details"""
    print_section("Test 5: Get Freelancer Details")
    
    if not test_data['freelancer_ids']:
        print_error("No available freelancer IDs")
        return False
    
    freelancer_id = test_data['freelancer_ids'][0]
    
    try:
        response = requests.get(f'{API_BASE}/api/freelancers/{freelancer_id}', timeout=5)
        
        if response.status_code == 200:
            freelancer = response.json()
            print_success(f"Retrieved freelancer details: {freelancer['name']}")
            print_info(f"\n  Basic Information:")
            print_info(f"    - ID: {freelancer['id']}")
            print_info(f"    - Email: {freelancer['email']}")
            print_info(f"    - Phone: {freelancer.get('phone', 'N/A')}")
            print_info(f"    - Location: {freelancer.get('location', 'N/A')}")
            
            print_info(f"\n  Professional Information:")
            print_info(f"    - Job Type: {freelancer.get('job_type', 'N/A')}")
            print_info(f"    - Skills: {freelancer.get('skills', 'N/A')}")
            print_info(f"    - About: {freelancer.get('about_me', 'N/A')[:50]}...")
            
            rating_info = freelancer.get('rating_info', {})
            print_info(f"\n  Rating Information:")
            print_info(f"    - Average Rating: {rating_info.get('average', 0):.2f}")
            print_info(f"    - Total Reviews: {rating_info.get('total_reviews', 0)}")
            
            recent_reviews = freelancer.get('recent_reviews', [])
            if recent_reviews:
                print_info(f"\n  Recent Reviews:")
                for review in recent_reviews[:2]:
                    print_info(f"    - {'⭐' * review['rating']} - {review.get('evaluator_name', 'N/A')}")
            
            return True
        else:
            print_error(f"Failed to retrieve freelancer details: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Exception retrieving freelancer details: {str(e)}")
        return False

def test_create_evaluators():
    """Test 6: Create Evaluators"""
    print_section("Test 6: Create Evaluators")
    
    evaluators = [
        {
            'name': 'David Wilson',
            'email': 'david.w@techcorp.com',
            'password': 'password123',
            'company': 'TechCorp Inc',
            'position': 'Technical Director'
        },
        {
            'name': 'Emily Davis',
            'email': 'emily.d@startupco.com',
            'password': 'password456',
            'company': 'StartupCo',
            'position': 'HR Manager'
        },
        {
            'name': 'James Brown',
            'email': 'james.b@innovate.com',
            'password': 'password789',
            'company': 'Innovate Labs',
            'position': 'Tech Lead'
        }
    ]
    
    success_count = 0
    for evaluator in evaluators:
        try:
            response = requests.post(
                f'{API_BASE}/api/evaluators',
                json=evaluator,
                timeout=5
            )
            
            if response.status_code == 201:
                data = response.json()
                evaluator_id = data.get('evaluator_id')
                test_data['evaluator_ids'].append({
                    'id': evaluator_id,
                    'password': evaluator['password']
                })
                print_success(f"Created evaluator: {evaluator['name']} (ID: {evaluator_id})")
                success_count += 1
            else:
                print_error(f"Failed to create evaluator: {evaluator['name']} - {response.text}")
        except Exception as e:
            print_error(f"Exception creating evaluator: {evaluator['name']} - {str(e)}")
    
    print_info(f"\nSuccessfully created {success_count}/{len(evaluators)} evaluators")
    return success_count > 0

def test_list_evaluators():
    """Test 7: List Evaluators"""
    print_section("Test 7: List Evaluators")
    
    try:
        response = requests.get(f'{API_BASE}/api/evaluators', timeout=5)
        
        if response.status_code == 200:
            evaluators = response.json()
            print_success(f"Retrieved evaluator list successfully, total: {len(evaluators)}")
            
            for evaluator in evaluators[:3]:
                print_info(f"\n  Evaluator: {evaluator['name']}")
                print_info(f"    - ID: {evaluator['id']}")
                print_info(f"    - Email: {evaluator['email']}")
                print_info(f"    - Company: {evaluator.get('company', 'N/A')}")
                print_info(f"    - Position: {evaluator.get('position', 'N/A')}")
                print_info(f"    - Evaluation Count: {evaluator.get('evaluation_count', 0)}")
            
            return True
        else:
            print_error(f"Failed to retrieve evaluator list: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Exception retrieving evaluator list: {str(e)}")
        return False

def test_verify_password():
    """Test 8: Verify Password"""
    print_section("Test 8: Verify Password")
    
    if not test_data['evaluator_ids']:
        print_error("No available evaluator IDs")
        return False
    
    evaluator = test_data['evaluator_ids'][0]
    
    # Test correct password
    try:
        response = requests.post(
            f'{API_BASE}/api/evaluators/verify-password',
            json={
                'evaluator_id': evaluator['id'],
                'password': evaluator['password']
            },
            timeout=5
        )
        
        if response.status_code == 200:
            print_success("Password verification successful (correct password)")
        else:
            print_error(f"Password verification failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Password verification exception: {str(e)}")
        return False
    
    # Test incorrect password
    try:
        response = requests.post(
            f'{API_BASE}/api/evaluators/verify-password',
            json={
                'evaluator_id': evaluator['id'],
                'password': 'wrong_password'
            },
            timeout=5
        )
        
        if response.status_code == 401:
            print_success("Password verification successful (incorrect password rejected)")
            return True
        else:
            print_error("Password verification failed (should reject incorrect password)")
            return False
    except Exception as e:
        print_error(f"Password verification exception: {str(e)}")
        return False

def test_create_ratings():
    """Test 9: Create Ratings"""
    print_section("Test 9: Create Ratings")
    
    if not test_data['freelancer_ids'] or not test_data['evaluator_ids']:
        print_error("Insufficient data to create ratings")
        return False
    
    ratings = [
        {
            'freelancer_id': test_data['freelancer_ids'][0],
            'evaluator_id': test_data['evaluator_ids'][0]['id'],
            'rating': 5,
            'review_text': 'Excellent candidate, strong technical skills and great communication'
        },
        {
            'freelancer_id': test_data['freelancer_ids'][0],
            'evaluator_id': test_data['evaluator_ids'][1]['id'],
            'rating': 4,
            'review_text': 'Good overall performance with room for improvement'
        },
        {
            'freelancer_id': test_data['freelancer_ids'][1],
            'evaluator_id': test_data['evaluator_ids'][0]['id'],
            'rating': 5,
            'review_text': 'Solid frontend skills, high quality work'
        }
    ]
    
    success_count = 0
    for rating in ratings:
        try:
            response = requests.post(
                f'{API_BASE}/api/ratings',
                json=rating,
                timeout=5
            )
            
            if response.status_code == 201:
                data = response.json()
                rating_id = data.get('rating_id')
                test_data['rating_ids'].append(rating_id)
                print_success(f"Created rating (ID: {rating_id})")
                print_info(f"  - Freelancer ID: {rating['freelancer_id']}")
                print_info(f"  - Rating: {'⭐' * rating['rating']}")
                success_count += 1
            else:
                print_error(f"Failed to create rating: {response.text}")
        except Exception as e:
            print_error(f"Exception creating rating: {str(e)}")
    
    print_info(f"\nSuccessfully created {success_count}/{len(ratings)} ratings")
    return success_count > 0

def test_get_freelancer_ratings():
    """Test 10: Get Freelancer Ratings"""
    print_section("Test 10: Get Freelancer Ratings")
    
    if not test_data['freelancer_ids']:
        print_error("No available freelancer IDs")
        return False
    
    freelancer_id = test_data['freelancer_ids'][0]
    
    try:
        response = requests.get(
            f'{API_BASE}/api/freelancers/{freelancer_id}/ratings',
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            rating_info = data.get('rating_info', {})
            reviews = data.get('reviews', [])
            rating_distribution = data.get('rating_distribution', {})
            
            print_success("Retrieved ratings successfully")
            print_info(f"\n  Rating Statistics:")
            print_info(f"    - Average Rating: {rating_info.get('average', 0):.2f}")
            print_info(f"    - Total Reviews: {rating_info.get('count', 0)}")
            
            print_info(f"\n  Rating Distribution:")
            for star in range(5, 0, -1):
                count = rating_distribution.get(str(star), 0)
                bar = '█' * count
                print_info(f"    {star}⭐: {bar} ({count})")
            
            print_info(f"\n  Review List:")
            for review in reviews[:3]:
                print_info(f"    - {'⭐' * review['rating']} {review.get('evaluator_name', 'N/A')}")
                if review.get('review_text'):
                    print_info(f"      \"{review['review_text'][:50]}...\"")
            
            return True
        else:
            print_error(f"Failed to retrieve ratings: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Exception retrieving ratings: {str(e)}")
        return False

def test_get_rating_statistics():
    """Test 11: Get Rating Statistics"""
    print_section("Test 11: Get Rating Statistics")
    
    if not test_data['freelancer_ids']:
        print_error("No available freelancer IDs")
        return False
    
    freelancer_id = test_data['freelancer_ids'][0]
    
    try:
        response = requests.get(
            f'{API_BASE}/api/freelancers/{freelancer_id}/rating-statistics',
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("Retrieved rating statistics successfully")
            print_info(f"\n  Average Rating: {data.get('average', 0):.2f}")
            print_info(f"  Total Reviews: {data.get('total_reviews', 0)}")
            
            print_info(f"\n  Detailed Distribution:")
            rating_breakdown = data.get('rating_breakdown', {})
            for star in range(5, 0, -1):
                info = rating_breakdown.get(str(star), {'count': 0, 'percentage': 0})
                count = info['count']
                percentage = info['percentage']
                bar = '█' * int(percentage / 5)
                print_info(f"    {star}⭐: {bar} {count} ({percentage:.1f}%)")
            
            return True
        else:
            print_error(f"Failed to retrieve rating statistics: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Exception retrieving rating statistics: {str(e)}")
        return False

def test_list_all_evaluations():
    """Test 12: List All Evaluations"""
    print_section("Test 12: List All Evaluations")
    
    try:
        response = requests.get(f'{API_BASE}/api/evaluations', timeout=5)
        
        if response.status_code == 200:
            evaluations = response.json()
            print_success(f"Retrieved all evaluation records successfully, total: {len(evaluations)}")
            
            for evaluation in evaluations[:3]:
                print_info(f"\n  Evaluation Record:")
                print_info(f"    - ID: {evaluation['id']}")
                print_info(f"    - Job Seeker: {evaluation.get('job_seeker_name', 'N/A')}")
                print_info(f"    - Evaluator: {evaluation.get('evaluator_name', 'N/A')}")
                print_info(f"    - Company: {evaluation.get('evaluator_company', 'N/A')}")
                print_info(f"    - Rating: {'⭐' * evaluation.get('rating', 0)}")
                print_info(f"    - Average Score: {evaluation.get('average_score', 0):.2f}")
            
            return True
        else:
            print_error(f"Failed to retrieve evaluation records: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Exception retrieving evaluation records: {str(e)}")
        return False

def test_update_freelancer():
    """Test 13: Update Freelancer"""
    print_section("Test 13: Update Freelancer")
    
    if not test_data['freelancer_ids']:
        print_error("No available freelancer IDs")
        return False
    
    freelancer_id = test_data['freelancer_ids'][0]
    
    update_data = {
        'availability': 'busy',
        'about_me': 'Updated bio: Experienced Python engineer with proven track record'
    }
    
    try:
        response = requests.put(
            f'{API_BASE}/api/freelancers/{freelancer_id}',
            json=update_data,
            timeout=5
        )
        
        if response.status_code == 200:
            print_success(f"Updated freelancer successfully (ID: {freelancer_id})")
            print_info(f"  - Updated fields: {', '.join(update_data.keys())}")
            return True
        else:
            print_error(f"Failed to update freelancer: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Exception updating freelancer: {str(e)}")
        return False

def test_duplicate_rating():
    """Test 14: Duplicate Rating (Should Fail)"""
    print_section("Test 14: Duplicate Rating (Should Fail)")
    
    if not test_data['freelancer_ids'] or not test_data['evaluator_ids']:
        print_error("Insufficient data to test duplicate rating")
        return False
    
    duplicate_rating = {
        'freelancer_id': test_data['freelancer_ids'][0],
        'evaluator_id': test_data['evaluator_ids'][0]['id'],
        'rating': 3,
        'review_text': 'This is a duplicate rating'
    }
    
    try:
        response = requests.post(
            f'{API_BASE}/api/ratings',
            json=duplicate_rating,
            timeout=5
        )
        
        if response.status_code == 400:
            print_success("Duplicate rating correctly rejected")
            print_info(f"  - Error message: {response.json().get('detail', 'N/A')}")
            return True
        else:
            print_error("Duplicate rating not rejected (should return 400)")
            return False
    except Exception as e:
        print_error(f"Exception testing duplicate rating: {str(e)}")
        return False

def test_invalid_data():
    """Test 15: Invalid Data (Should Fail)"""
    print_section("Test 15: Invalid Data (Should Fail)")
    
    # Test creating freelancer with missing required fields
    invalid_freelancer = {
        'phone': '+1-555-0000'
        # Missing name and email
    }
    
    try:
        response = requests.post(
            f'{API_BASE}/api/freelancers',
            json=invalid_freelancer,
            timeout=5
        )
        
        if response.status_code == 422:
            print_success("Invalid data correctly rejected (missing required fields)")
            return True
        else:
            print_error("Invalid data not rejected")
            return False
    except Exception as e:
        print_error(f"Exception testing invalid data: {str(e)}")
        return False

def test_nonexistent_resource():
    """Test 16: Access Nonexistent Resource (Should Return 404)"""
    print_section("Test 16: Access Nonexistent Resource (Should Return 404)")
    
    try:
        response = requests.get(f'{API_BASE}/api/freelancers/99999', timeout=5)
        
        if response.status_code == 404:
            print_success("Nonexistent resource returns 404")
            print_info(f"  - Error message: {response.json().get('detail', 'N/A')}")
            return True
        else:
            print_error(f"Nonexistent resource returned wrong status code: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Exception testing nonexistent resource: {str(e)}")
        return False

def test_page_access():
    """Test 17: Access HTML Pages"""
    print_section("Test 17: Access HTML Pages")
    
    pages = [
        ('/', 'Home Page'),
        ('/admin', 'Admin Dashboard'),
        ('/job_seeker_register.html', 'Job Seeker Registration'),
        ('/evaluator_register.html', 'Evaluator Registration'),
        ('/talent_market.html', 'Talent Market')
    ]
    
    success_count = 0
    for path, name in pages:
        try:
            response = requests.get(f'{API_BASE}{path}', timeout=5)
            
            if response.status_code == 200 and 'text/html' in response.headers.get('content-type', ''):
                print_success(f"{name} accessed successfully")
                success_count += 1
            else:
                print_error(f"{name} access failed: {response.status_code}")
        except Exception as e:
            print_error(f"{name} access exception: {str(e)}")
    
    print_info(f"\nSuccessfully accessed {success_count}/{len(pages)} pages")
    return success_count == len(pages)

def cleanup_test_data():
    """Cleanup Test Data"""
    print_section("Cleanup Test Data")
    
    # Delete created freelancers (will cascade delete ratings)
    deleted_count = 0
    for freelancer_id in test_data['freelancer_ids']:
        try:
            response = requests.delete(f'{API_BASE}/api/freelancers/{freelancer_id}', timeout=5)
            if response.status_code == 200:
                deleted_count += 1
        except:
            pass
    
    print_info(f"Deleted {deleted_count} test freelancers")
    print_info("Note: Evaluator data not deleted (no delete endpoint available)")

def main():
    """Main test function"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║                                                           ║")
    print("║     Free Recruitment Market - Complete Test Suite        ║")
    print("║                                                           ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}\n")
    
    print_info(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print_info(f"API URL: {API_BASE}")
    print_info("Starting tests...\n")
    
    tests = [
        ("Health Check", test_health_check),
        ("Root Endpoint", test_root_endpoint),
        ("Create Freelancers", test_create_freelancers),
        ("List Freelancers", test_list_freelancers),
        ("Get Freelancer Details", test_get_freelancer_detail),
        ("Create Evaluators", test_create_evaluators),
        ("List Evaluators", test_list_evaluators),
        ("Verify Password", test_verify_password),
        ("Create Ratings", test_create_ratings),
        ("Get Freelancer Ratings", test_get_freelancer_ratings),
        ("Get Rating Statistics", test_get_rating_statistics),
        ("List All Evaluations", test_list_all_evaluations),
        ("Update Freelancer", test_update_freelancer),
        ("Duplicate Rating (Should Fail)", test_duplicate_rating),
        ("Invalid Data (Should Fail)", test_invalid_data),
        ("Nonexistent Resource (Should 404)", test_nonexistent_resource),
        ("Access HTML Pages", test_page_access)
    ]
    
    results = []
    start_time = time.time()
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
            time.sleep(0.5)  # Avoid making requests too quickly
        except Exception as e:
            print_error(f"Uncaught exception in test '{name}': {str(e)}")
            results.append((name, False))
    
    end_time = time.time()
    
    # Print test summary
    print_section("Test Summary")
    
    passed = sum(1 for _, result in results if result)
    failed = len(results) - passed
    
    print(f"{Colors.BOLD}Test Results:{Colors.RESET}")
    for name, result in results:
        status = f"{Colors.GREEN}✓ PASS{Colors.RESET}" if result else f"{Colors.RED}✗ FAIL{Colors.RESET}"
        print(f"  {status} - {name}")
    
    print(f"\n{Colors.BOLD}Statistics:{Colors.RESET}")
    print(f"  Total Tests: {len(results)}")
    print(f"  {Colors.GREEN}Passed: {passed}{Colors.RESET}")
    print(f"  {Colors.RED}Failed: {failed}{Colors.RESET}")
    print(f"  Success Rate: {(passed/len(results)*100):.1f}%")
    print(f"  Total Time: {(end_time - start_time):.2f} seconds")
    
    # Ask whether to cleanup test data
    print(f"\n{Colors.YELLOW}Cleanup test data? (y/n): {Colors.RESET}", end='')
    try:
        choice = input().strip().lower()
        if choice == 'y':
            cleanup_test_data()
        else:
            print_info("Skipped data cleanup")
    except:
        print_info("\nSkipped data cleanup")
    
    print(f"\n{Colors.BOLD}{Colors.CYAN}Testing completed!{Colors.RESET}\n")
    
    return passed == len(results)

if __name__ == '__main__':
    try:
        success = main()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Testing interrupted by user{Colors.RESET}\n")
        exit(1)
    except Exception as e:
        print(f"\n\n{Colors.RED}Fatal error in testing: {str(e)}{Colors.RESET}\n")
        exit(1)