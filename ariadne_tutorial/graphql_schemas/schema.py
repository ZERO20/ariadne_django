import datetime

from ariadne import gql, QueryType, make_executable_schema, ObjectType


# gql function to validate schema
type_defs = gql("""
    scalar DateTime

    type Query {
        hello: String!
        time: DateTime!
    }
""")

# Create type instance for Query type defined in our schema...
query = QueryType()


# ...and assign our resolver function to its "hello" field.
@query.field("hello")
def resolve_hello(_, info):
    request = info.context['request']
    user_agent = request.headers.get("user-agent", "guest")
    return f"Hello {user_agent}!"


@query.field("time")
def resolver_current_time(*_):
    return datetime.datetime.now()


schema = make_executable_schema(type_defs, query)
