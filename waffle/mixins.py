from functools import partial

from django.http import Http404

from waffle import switch_is_active, flag_is_active, sample_is_active


class BaseFeatureMixin(object):

    def validate_feature(self, feature, func):
        if feature.startswith('!'):
            active = not func(feature[1:])
        else:
            active = func(feature)
        return active

    def invalid_feature(self):
        raise Http404


class FeatureFlagMixin(BaseFeatureMixin):
    """
    Checks that as flag is active, or 404. Operates like the FBV decorator
    feature_flag
    """

    feature_flag = None

    def dispatch(self, request, *args, **kwargs):
        func = partial(flag_is_active, request)
        active = self.validate_feature(self.feature_flag, func)

        if not active:
            return self.invalid_feature()

        return super(FeatureFlagMixin, self).dispatch(request, *args, **kwargs)


class FeatureSampleMixin(BaseFeatureMixin):
    """
    Checks that as switch is active, or 404. Operates like the FBV decorator
    feature_sample.
    """

    feature_sample = None

    def dispatch(self, request, *args, **kwargs):
        active = self.validate_feature(self.feature_sample, sample_is_active)

        if not active:
            return self.invalid_feature()

        return super(FeatureSampleMixin, self).dispatch(request, *args, **kwargs)


class FeatureSwitchMixin(BaseFeatureMixin):
    """
    Checks that as switch is active, or 404. Operates like the FBV decorator
    feature_switch.
    """

    feature_switch = None

    def dispatch(self, request, *args, **kwargs):
        active = self.validate_feature(self.feature_switch, switch_is_active)

        if not active:
            return self.invalid_feature()

        return super(FeatureSwitchMixin, self).dispatch(request, *args, **kwargs)
