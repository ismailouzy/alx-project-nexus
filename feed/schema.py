import graphene
from graphene_django import DjangoObjectType
from .models import Post, Comment, Interaction


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = (
                'id',
                'content', 'author', 'created', 'comments')


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'content', 'created')


class InteractionType(DjangoObjectType):
    class Meta:
        model = Interaction
        fields = ('id', 'post', 'user', 'Interaction_type', 'created')


class Query(graphene.ObjectType):
    all_posts = graphene.List(PostType)
    post_by_id = graphene.Field(PostType, id=graphene.Int(required=True))
    user_posts = graphene.List(
            PostType, username=graphene.String(required=True))

    def resolve_all_posts(self, info):
        return Post.objects.all().order_by('-created')

    def resolve_by_id(self, info, id):
        return Post.objects.get(id=id)


class CreatePost(graphene.Mutation):
    post = graphene.Field(PostType)

    class Arguments:
        content = graphene.String(required=True)

    def mutate(self, info, content):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("You need to authenticate")
        post = Post(content=content, author=user)
        post.save()
        return CreatePost(post=post)


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
