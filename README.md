
# Getting started

## Tornado Apps (FFWeb or WWW-Purchase)

### Install Dependencies

1. Install [homebrew](http://brew.sh).

        ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

1. Install global dependencies

        brew install node yarn
        sudo easy_install virtualenv virtualenvwrapper

1. Run setup script

        ./setup <app_name> dev

        #Examples:
        ./setup ffweb dev
        ./setup purchase dev
        ./setup www dev

        The 'dev' specifies that you will be setting ENV variables for tornado_discovery.py to use when looking up api host endpoints and other environment-specific settings. When you choose 'dev', you are setting ENV variables that point to QA api servers.

### Run

1. Activate virtualenv

        source activate-<app_name>

        #Examples:
        source activate-ffweb
        source activate-purchase

1. Compile assets

        gulp build

    or to watch for changes and automatically recompile:

        gulp

1. Run tornado or Run django
        # Tornado
        ./launch.py <app_name>

        #Examples:
        ./launch.py ffweb
        ./launch.py purchase
        ./launch.py all

        # Django (non-purchase WWW)
        ./manage.py runserver

1. Open your browser and go to [http://localhost:8100](http://localhost:8100) for tornado (ffweb and purchase) or [http://localhost:8000](http://localhost:800) for Django.

### Clean Up

1. Whenever you want to clean up and start fresh, either recheckout the repo, or run the following:

        git clean -xdf
        git reset --hard

# Javascript Conventions

For all Javascript Style conventions, we default to [Airbnb's](https://github.com/airbnb/javascript) style guide unless specifically pointed out in this doc.

## Flux

### Ajax:

For all AJAX requests to a web service, call the Web API directly from the *Action Creator*
and then make the API dispatch the event with the result to as a payload.
![React AJAX](https://github.com/facebook/flux/raw/master/docs/img/flux-diagram-white-background.png =250x)
[Async Requests with React JS](http://www.code-experience.com/async-requests-with-react-js-and-flux-revisited/)

A quote from Bill Fisher:

"XHR output (saving to the server) should happen in the action creator.  After calling the dispatcher method -- which would be dispatch(), or another wrapper of dispatch() as in the example -- you would then call a utility module that would encapsulate your XHR mechanics.  We call these Utils files.  In the new chat example, you will see this exemplified as ChatWebAPIUtils.js.
XHR input (data coming from the server) should happen in the success or failure callbacks to the XHR call.  Within that callback, I would invoke another action creator, but Jing told me that she sometimes just calls dispatch() directly at that point.  I prefer the formality of keeping similar operations in one place, so I would call an action creator.
You can see an example of calling the ChatWebAPIUtils method here: https://github.com/facebook/flux/blob/master/examples/flux-chat/js/actions/ChatMessageActionCreators.js#L28 "
[https://groups.google.com/forum/#!msg/reactjs/jBPHH4Q-8Sc/93LMQIt4RmsJ](https://groups.google.com/forum/#!msg/reactjs/jBPHH4Q-8Sc/93LMQIt4RmsJ)