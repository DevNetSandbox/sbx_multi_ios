# -*- mode: python; python-indent: 4 -*-
import ncs
from ncs.application import Service
import ncs.experimental
from .notifications import send_webex_teams


class ServiceCallbacks(Service):

    # The create() callback is invoked inside NCS FASTMAP and
    # must always exist.
    @Service.create
    def cb_create(self, tctx, root, service, proplist):
        self.log.info('Service create(service=', service._path, ')')


class WebexTeamsSubscriber(ncs.experimental.Subscriber):
    """This subscriber subscribes to changes in the..."""

    # custom initializer which gets called from the
    # constructor (__int__)
    def init(self):
        # data structure to store notification mappings
        self.subscriptions = dict()

        with ncs.maapi.single_read_trans('admin', 'webex_teams') as t:
            self.log.info('starting subscriber')

            with ncs.maapi.single_read_trans('admin', 'test_context') as t:
                root = ncs.maagic.get_root(t)
                self.api_token = root.webex_teams.api_token
                self.room_id = root.webex_teams.room_id
                if root.webex_teams.keypath:
                    self.keypath = root.webex_teams.keypath
            if self.keypath:
                self.register(self.keypath, priority=100)
                
            self.log.info("Token: {}".format(self.api_token))
            self.log.info("Room: {}".format(self.room_id))

    # Initate your local state
    def pre_iterate(self):
        self.log.info('DemoSubscriber: pre_iterate')
        return []

    # Iterate over the change set
    def iterate(self, keypath, op, oldval, newval, state):
        state.append((str(keypath), op, str(oldval), str(newval)))
        return ncs.ITER_RECURSE

    # This will run in a separate thread to avoid a transaction deadlock
    def post_iterate(self, state):
        self.log.info('DemoSubscriber: post_iterate, state=', state)
        send_webex_teams(self.api_token, self.room_id, state)
        pass

    # determine if post_iterate() should run
    def should_post_iterate(self, state):
        return state != []


# ---------------------------------------------
# COMPONENT THREAD THAT WILL BE STARTED BY NCS.
# ---------------------------------------------
class Main(ncs.application.Application):
    def setup(self):
        # The application class sets up logging for us. It is accessible
        # through 'self.log' and is a ncs.log.Log instance.
        self.log.info('Main RUNNING')

        # Service callbacks require a registration for a 'service point',
        # as specified in the corresponding data model.
        #
        self.register_service('webex-teams-servicepoint', ServiceCallbacks)

        # Create your subscriber
        self.sub = WebexTeamsSubscriber(app=self)
        self.sub.start()

        # If we registered any callback(s) above, the Application class
        # took care of creating a daemon (related to the service/action point).

        # When this setup method is finished, all registrations are
        # considered done and the application is 'started'.

    def teardown(self):
        # When the application is finished (which would happen if NCS went
        # down, packages were reloaded or some error occurred) this teardown
        # method will be called.

        self.sub.stop()

        self.log.info('Main FINISHED')
