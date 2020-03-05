Feature: As a website user,
             I want to add a build

    Scenario: Add build
       Given app is setup
        When i add a build
        Then i should get 201
