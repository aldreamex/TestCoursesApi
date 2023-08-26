import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Student, Course


@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory

@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory

@pytest.mark.django_db
def test_get_course_retrieve(client, course_factory):

    # Arrange
    courses = course_factory()

    # Act
    response = client.get(f'/api/v1/courses/{courses.id}/')

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == courses.id

@pytest.mark.django_db
def test_get_course_list(client, course_factory):

    # Arrange
    courses = course_factory(_quantity=10)

    # Act
    response = client.get(f'/api/v1/courses/')

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 10

@pytest.mark.django_db
def test_get_course_filter_id(client, course_factory):

    # Arrange
    courses = course_factory(_quantity=10)
    target_course = courses[5]

    # Act
    response = client.get(f'/api/v1/courses/?id={target_course.id}')

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['id'] == target_course.id

@pytest.mark.django_db
def test_get_course_filter_name(client, course_factory):

    # Arrange
    courses = course_factory(_quantity=10)
    target_course = course_factory(name='Examplename')

    # Act
    response = client.get(f'/api/v1/courses/?name={target_course.name}')

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['name'] == target_course.name


@pytest.mark.django_db
def test_successful_creation_course(client, course_factory):

    # Arrange
    count = Course.objects.count()

    # Act
    response = client.post(f'/api/v1/courses/', data={
        "name": "New Course",
        "students": []
    })

    # Assert
    assert response.status_code == 201
    assert Course.objects.count() == count + 1

@pytest.mark.django_db
def test_successful_update_course(client, course_factory):

    # Arrange
    courses = course_factory()
    updated_data = {
        "name": "New Course update",
        "students": []
    }

    # Act
    response = client.put(f'/api/v1/courses/{courses.id}/', data=updated_data)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == updated_data['name']
    assert Course.objects.filter(name=updated_data['name']).exists()
    assert 'students' in data
    assert data['students'] == updated_data['students']

@pytest.mark.django_db
def test_successful_delete_course(client, course_factory):

    # Arrange
    courses = course_factory()

    # Act
    response = client.delete(f'/api/v1/courses/{courses.id}/')

    # Assert
    assert response.status_code == 204
    # assert not response.content
    assert response.content == b''