import connexion
from swagger_server.models.domain import Domain as ApiDomain
from swagger_server.models.domain_create import DomainCreate as ApiDomainCreate

from models import Domain as SqlAlchemyDomain


def domain_create(data=None):  # noqa: E501
    """domain_create
     # noqa: E501
    :param data:
    :type data: dict | bytes
    :rtype: Domain
    """
    # Unpack the request body
    if connexion.request.is_json:
        body = connexion.request.get_json()

    # Validate that the body is a valid ApiDomainCreate request
    create_request = ApiDomainCreate.from_dict(body)
    # Apply transformation (when required)
    transformed_create_request = CREATE_REQUEST_TRANSFORMATION.apply(
        create_request)
    # The transformed dictionary is used to construct an SqlAlchemyDomain
    # instance.
    domain = SqlAlchemyDomain(**transformed_create_request)
    # Save the domain
    db.add(domain)  # This should populate values like id, created_at, etc.
    db.commit()
    # Transform the SqlAlchemyDomain to a dict
    response_dict = altus_convert_function(domain)
    # Apply transformation (when required)
    transformed_response_dict = CREATE_RESPONSE_TRANSFORMATION.apply(
        response_dict)
    # Construct the model that is required in the response
    response = ApiDomain.from_dict(transformed_response_dict)
    return response


def domain_read(domain_id):  # noqa: E501
    """domain_read
     # noqa: E501
    :param domain_id: A unique integer value identifying the domain.
    :type domain_id: int
    :rtype: Domain
    """
    domain = db.domain.get(id=domain_id)  # Not sure about syntax here
    # Transform the SqlAlchemyDomain to a dict
    response_dict = altus_convert_function(domain)
    # Apply transformation (when required)
    transformed_response_dict = RESPONSE_TRANSFORMATION.apply(
        response_dict)
    # Construct the model that is required in the response
    response = ApiDomain.from_dict(transformed_response_dict)
    return response

