from ariadne import gql, QueryType, make_executable_schema


# gql function to validate schema
type_defs = gql("""
    type Query {
        hello: String!
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


schema = make_executable_schema(type_defs, query)
