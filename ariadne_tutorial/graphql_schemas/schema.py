import datetime

from ariadne import gql, ObjectType, QueryType, make_executable_schema


# gql function to validate schema
type_defs = gql("""
    scalar DateTime

    type Query {
        hello: String!
        time: DateTime!
        user: User,
        client: Client,
    }

    type User {
        username: String!
        email: String!
    }

    type Client{
        email: String!
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


@query.field("user")
@query.field('client')
def resolve_user(_, info):
    return info.context["request"].user


# add resolvers for another type
user = ObjectType("User")
client = ObjectType("Client")


@user.field("username")
def resolve_username(obj, *_):
    return f'{obj.first_name} {obj.last_name}'


@user.field("email")
@client.field("email")
def resolve_email(obj, *_):
    return f'{obj.email}'


schema = make_executable_schema(type_defs, query, user, client)
