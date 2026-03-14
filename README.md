# Modular Entity and Mapping System

This project is a Django REST Framework backend built for managing Vendors, Products, Courses, Certifications, and their mappings. It follows a strictly modular architecture where each entity and mapping resides in its own Django app.

## Mandatory Technical Constraints
- Built using **APIView only** (No ViewSets, GenericAPIViews, or Mixins).
- Explicit URL routing (No Routers).
- API Documentation generated using **drf-yasg**.
- Modular architecture with separate apps for each entity and mapping.

## Apps Structure
### Master Apps
- `vendor`
- `product`
- `course`
- `certification`

### Mapping Apps
- `vendor_product_mapping`
- `product_course_mapping`
- `course_certification_mapping`

## Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Seed Initial Data**
   ```bash
   python manage.py seed_data
   ```

4. **Run Tests**
   ```bash
   python manage.py test vendor
   ```

5. **Run Server**
   ```bash
   python manage.py runserver
   ```

## API Documentation
Once the server is running, you can access the documentation at:
- **Swagger UI**: [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)
- **ReDoc**: [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)

## Key Features

- **Advanced Engineering (Stand-out Details)**:
  - **Global Exception Handling**: Custom uniform error responses for all API endpoints (see `core/exceptions.py`).
  - **Automated Data Integrity**: Models automatically enforce a single `primary_mapping=True` per parent by resetting old primaries on save.
  - **Query Optimization**: Implemented `select_related()` in mapping views to solve the N+1 query problem and improve performance.
- **Validation Rules**:
  - Unique `code` for master records.
  - Duplicate mapping prevention using `unique_together` constraints.
- **Filtering**:
  - Supports query-param based filtering (e.g., `/api/vendor-product-mappings/?vendor_id=1`).
- **Soft Delete**: Uses `is_active` field for consistent record management.
- **Modularity**: Strictly decoupled apps, each with its own models, serializers, views, and URL routing.
