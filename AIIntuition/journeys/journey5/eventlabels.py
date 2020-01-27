from typing import List


class EventLabels:
    @classmethod
    def task_labels(cls,
                    as_feature_labels: bool = False) -> List[str]:
        if as_feature_labels:
            labels = ['',
                      '',
                      '',
                      '',
                      '',
                      '',
                      '',
                      '',
                      '',
                      '']
        else:
            labels = ['Task: ',
                      'Profile: ',
                      'Pref Core: ',
                      'Load Factor: ',
                      'Curr Mem: ',
                      'Run Time: ',
                      'Deficit: ',
                      'Cost: ',
                      'Time Left: ',
                      'Done: ']
        return labels

    @classmethod
    def host_labels(cls,
                    as_feature_labels: bool = False) -> List[str]:
        if as_feature_labels:
            labels = ['',
                      '',
                      '',
                      '',
                      '',
                      '',
                      '',
                      '',
                      '',
                      '',
                      '']
        else:
            labels = ['DC: ',
                      'Host: ',
                      'Type: ',
                      'cores: ',
                      'Mem: ',
                      'Mem Util %: ',
                      'Comp: ',
                      'Comp Util %: ',
                      'Num Tasks: ',
                      'Local Day: ',
                      'Local Hour: ']
        return labels

    @classmethod
    def exception_labels(cls,
                         as_feature_labels: bool = False) -> List[str]:
        if as_feature_labels:
            labels = ['']
        else:
            labels = ['Error: ']
        return labels
