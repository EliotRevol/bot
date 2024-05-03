from abc import ABC, abstractmethod

from experiments.base import ExperimentNotFound
from experiments.election import WelcomeElectionExperiment, WelcomeWalkElectionExperiment, \
    NationalNewsFetchElectionExperiment, NationalNewsWalkElectionExperiment, ChannelPersonalizationElectionExperiment
from experiments.generic import WelcomeWalkExperiment, ResolveExperiment, ChannelWalkExperiment, TestExperiment, \
    ChannelPersonalizationExperiment, WelcomeWatchExperiment
from experiments.meta import MetaChannelPersonalization, MetaWalk


class ExperimentFactory(ABC):
    """
    Abstract Factory class for experiments, generate experiment suites regarding experiment name and naming
    """

    @abstractmethod
    def create_experiment(self, **kwargs): """
    Abstract method for creating experiments, 
        :param kwargs: Arguments
        :return: 
        """


class GenericExperimentFactory(ExperimentFactory):
    def create_experiment(self, **kwargs):
        experiment_name = kwargs['experiment']
        if experiment_name == "welcome-walk":
            return WelcomeWalkExperiment(**kwargs)
        elif experiment_name == "resolve":
            return ResolveExperiment(**kwargs)
        elif experiment_name == "channel-walk":
            return ChannelWalkExperiment(**kwargs)
        elif experiment_name == "expe0":
            return TestExperiment(**kwargs)
        elif experiment_name == "channel-personalization":
            return ChannelPersonalizationExperiment(**kwargs)
        elif experiment_name == "welcome-watch":
            return WelcomeWatchExperiment(**kwargs)
        else:
            raise ExperimentNotFound


class ElectionExperimentFactory(ExperimentFactory):

    def create_experiment(self, **kwargs):
        experiment_name = kwargs['experiment']
        if experiment_name == "election-welcome-fetch":
            return WelcomeElectionExperiment(**kwargs)
        elif experiment_name == "election-welcome-walk":
            return WelcomeWalkElectionExperiment(**kwargs)
        elif experiment_name == "election-national-news-fetch":
            return NationalNewsFetchElectionExperiment(**kwargs)
        elif experiment_name == "election-national-news-walk":
            return NationalNewsWalkElectionExperiment(**kwargs)
        elif experiment_name == "election-channel-personalization":
            return ChannelPersonalizationElectionExperiment(**kwargs)
        else:
            raise ExperimentNotFound


class MetaExperimentFactory(ExperimentFactory):

    def create_experiment(self, **kwargs):
        experiment_name = kwargs['experiment']
        if experiment_name == "meta-channel-personalization":
            return MetaChannelPersonalization(**kwargs)
        elif experiment_name == "meta-walk":
            return MetaWalk(**kwargs)
        else:
            raise ExperimentNotFound
