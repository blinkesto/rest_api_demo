from behave import given, when, then

# https://github.com/ismaild/flaskr-bdd/blob/master/features/steps/flaskr_steps.py

@given(u'app is setup')
def flask_setup(context):
    assert context.client and context.db

@given(u'i add a build')
@when(u'i add a build')
def step_impl(context):
    context.page = context.client.post('/api/build/builds/', json={
        'number': '1001', 'servers': []
    }
    )
    assert context.page

@then(u'i should get 201')
def success(context):
    print context.page.status
    assert "201" in context.page.status
