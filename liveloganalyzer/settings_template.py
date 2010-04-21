"""
Important note: the name of the mongoDB "collection" is what links a "source"
with an "analyzer". So for an analyzer to use the data from a source, the name
of the collection must be the same in SOURCES_SETTINGS and ANALYSIS_SETTINGS.
"""

from sources import (SourceLog, MysqladminExtendedRelativeSource,
                     MysqladminExtendedAbsoluteSource, VmstatSource, DfSource,
                     )
from parsers import (NginxCacheParser, MysqladminExtendedRelativeParser,
                     MysqladminExtendedAbsoluteParser, PhpErrorParser, SyslogParser,
                     VmstatParser, DfParser,
                     )
from analyzers import (CacheStatus, Upstream5xxStatus, AvgUpstreamResponseTimePerServer,
                       RequestsPerMinuteByType, MysqlQuestionsPerSecond,
                       MysqlSlowQueriesPerSecond, WordpressLoggedIn, PhpErrorCountByServer,
                       SyslogCountByServerAndProcess, GenericAverageValueAnalyzer,
                       WordpressLoggedInByUser, AvgUpstreamResponseTimePerServerLoggedIn,
                       )
MONGODB_NAME = 'mydb'
PROCESSED_MAX_SIZE = 1 # in megabytes
MAX_COLLECTION_SIZE = 5 # in megabytes
NG_CACHE_COLL = 'ng_cache'
SYSLOG_COLL = 'syslog'
PHP_ERROR_COLL = 'php_error'
MYSQL_COLL = 'mysql_extended'
SYSTEM_COLL = 'system'

SOURCES_SETTINGS = [
    {'source': (SourceLog, {'host': 'us-ng1', 'filepath': '/var/log/nginx/cache.log', 'encoding': 'latin-1',}),
     'parser': NginxCacheParser,
     'collection': NG_CACHE_COLL,
     },
    {'source': (SourceLog, {'host': 'us-ng2', 'filepath': '/var/log/nginx/cache.log', 'encoding': 'latin-1',}),
     'parser': NginxCacheParser,
     'collection': NG_CACHE_COLL,
     },
    {'source': (SourceLog, {'host': 'us-ng3', 'filepath': '/var/log/nginx/cache.log', 'encoding': 'latin-1',}),
     'parser': NginxCacheParser,
     'collection': NG_CACHE_COLL,
     },
    {'source': (SourceLog, {'host': 'us-apa1', 'filepath': '/var/log/PHP_errors.log', 'encoding': 'latin-1',}),
     'parser': PhpErrorParser,
     'collection': PHP_ERROR_COLL,
     },
    {'source': (SourceLog, {'host': 'us-apa2', 'filepath': '/var/log/PHP_errors.log', 'encoding': 'latin-1',}),
     'parser': PhpErrorParser,
     'collection': PHP_ERROR_COLL,
     },
    {'source': (SourceLog, {'host': 'us-apa3', 'filepath': '/var/log/PHP_errors.log', 'encoding': 'latin-1',}),
     'parser': PhpErrorParser,
     'collection': PHP_ERROR_COLL,
     },
    {'source': (MysqladminExtendedRelativeSource, {'host': 'us-my1',}),
     'parser': MysqladminExtendedRelativeParser,
     'collection': MYSQL_COLL,
     },
    {'source': (DfSource, {'host': 'us-my1', 'filepath': '/mnt',}),
     'parser': DfParser,
     'collection': SYSTEM_COLL,
     },
    ]

PLOT_SET = {
    'rpm': {
        'label': 'Requests/min',
        'format': '%d',
        'collection': NG_CACHE_COLL,
        # 'window_length': 120,
        'analyzers': [
            (RequestsPerMinuteByType, {'media': '1'}),
            (RequestsPerMinuteByType, {'media': '0'}),
            ],
        },
    'cache0': {
        'label': 'Cache status (non-media)',
        'format': '%.1f%%',
        'collection': NG_CACHE_COLL,
        'flot_options': {'yaxis': {'max': 100,},},
        'analyzers': [
            (CacheStatus, {'status': 'HIT', 'media': '0'}),
            (CacheStatus, {'status': 'MISS', 'media': '0'}),
            (CacheStatus, {'status': 'EXPIRED', 'media': '0'}),
            (CacheStatus, {'status': 'UPDATING', 'media': '0'}),
            (CacheStatus, {'status': 'STALE', 'media': '0'}),
            ],
        },
    'cache1': {
        'label': 'Cache status (media)',
        'format': '%.1f%%',
        'collection': NG_CACHE_COLL,
        'flot_options': {'yaxis': {'min': 50, 'max': 100,},},
        'analyzers': [
            (CacheStatus, {'status': 'HIT', 'media': '1'}),
            (CacheStatus, {'status': 'MISS', 'media': '1'}),
            (CacheStatus, {'status': 'EXPIRED', 'media': '1'}),
            (CacheStatus, {'status': 'UPDATING', 'media': '1'}),
            (CacheStatus, {'status': 'STALE', 'media': '1'}),
            ],
        },
    'http_status': {
        'label': 'HTTP Status',
        'format': '%d',
        'collection': NG_CACHE_COLL,
        'analyzers': [
            (Upstream5xxStatus, {}),
            ],
        },
    'wp_login': {
        'label': 'WP logged in',
        'format': '%d',
        'collection': NG_CACHE_COLL,
        'analyzers': [
            (WordpressLoggedInByUser, {'wp_user': r'eric\.yates'}),
            (WordpressLoggedIn, {}),
            ],
        },
    'php_error': {
        'label': 'PHP error count',
        'format': '%d',
        'collection': PHP_ERROR_COLL,
        'analyzers': [
            (PhpErrorCountByServer, {'server': 'us-apa1'}),
            (PhpErrorCountByServer, {'server': 'us-apa2'}),
            (PhpErrorCountByServer, {'server': 'us-apa3'}),
            ],
        },
    'aurt': {
        'label': 'Avg Upstream Resp Time',
        'format': '%.2f',
        'collection': NG_CACHE_COLL,
        'analyzers': [
            (AvgUpstreamResponseTimePerServerLoggedIn, {'logged_in': r'^\s*$',}),
            ],
        },
    'aurtli': {
        'label': 'Avg Upstream Resp Time Logged In',
        'format': '%.2f',
        'collection': NG_CACHE_COLL,
        'analyzers': [
            (AvgUpstreamResponseTimePerServerLoggedIn, {'logged_in': r'wordpress_logged_in_',}),
            ],
        },
    'mysql': {
        'label': 'MySQL Questions/sec',
        'format': '%.1f',
        'collection': MYSQL_COLL,
        'flot_options': {'yaxis': {'max': 4100,},},
        'analyzers': [
            (MysqlQuestionsPerSecond, {'server': 'us-my1'}),
            (MysqlQuestionsPerSecond, {'server': 'us-my2'}),
            ],
        },
    'df': {
        'label': 'Disk Usage',
        'format': '%.1f',
        'collection': SYSTEM_COLL,
        'flot_options': {'yaxis': {'max': 100,},},
        'analyzers': [
            (GenericAverageValueAnalyzer, {'server': 'us-my1', 'parameter': 'df_use_percent',}),
            ]
        },
    }

ANALYSIS_SETTINGS = {
    'channel_name': '/topic/graph',
    'time_periods': [
        {'interval': 5*60,                 # in seconds
         'history_length': 144,        # number of processed data points to save
         'default_window_length': 5*60+5,        # in seconds
         'default_flot_options': {
                'series': {'stack': 0,
                           'bars': {'show': True, 'barWidth': (5*60)*(0.8*1000), 'lineWidth': 1,},},
                'xaxis': {'mode': "time",
                          'timeformat': "%H:%M",
                          'labelWidth': 20,
                          'labelHeight': 8,
                          },
                'yaxis': {'min': 0,
                          },
                },
         'groups': PLOT_SET,
         },
        {'interval': 5,                 # in seconds
         'history_length': 60,        # number of processed data points to save
         'default_window_length': 29,        # in seconds
         'default_flot_options': {
                'series': {'stack': 0,
                           'bars': {'show': True, 'barWidth': (5)*(0.8*1000), 'lineWidth': 1,},},
                'xaxis': {'mode': "time",
                          'timeformat': ":%M",
                          'labelWidth': 20,
                          'labelHeight': 8,
                          },
                'yaxis': {'min': 0,
                          },
                },
         'groups': PLOT_SET,
         },
        ],
    }
