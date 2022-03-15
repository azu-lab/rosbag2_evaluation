#必要なライブラリをインポート
library(dplyr)
library(ggplot2)
library(scales)

#x軸の各ラベル名
xaxis_scale = c("RadarDetection","Range", "NavSatFix",  "RadarTrack","PointCloud512k", "PointCloud1m", "PointCloud2m","PointCloud4m")
v_label = c("default (1,000 B)", "1 MiB","10 MiB","100 MiB")
box_cols <- c("#f7f7f7", "#cccccc","#969696","#525252")                # box colors

d1 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output_play/nd=false:mcs=0:spp=default/RadarDetection:rate=15/QoS=volatile,reliable:DDS=rmw_cyclonedds_cpp/raqs=default:rate=default/jitter_ms.txt")
d2 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output_play/nd=false:mcs=0:spp=default/Range:rate=15/QoS=volatile,reliable:DDS=rmw_cyclonedds_cpp/raqs=default:rate=default/jitter_ms.txt")
d3 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output_play/nd=false:mcs=0:spp=default/NavSatFix:rate=15/QoS=volatile,reliable:DDS=rmw_cyclonedds_cpp/raqs=default:rate=default/jitter_ms.txt")
d4 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output_play/nd=false:mcs=0:spp=default/RadarTrack:rate=15/QoS=volatile,reliable:DDS=rmw_cyclonedds_cpp/raqs=default:rate=default/jitter_ms.txt")
d5 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output_play/nd=false:mcs=0:spp=default/PointCloud512k:rate=15/QoS=volatile,reliable:DDS=rmw_cyclonedds_cpp/raqs=default:rate=default/jitter_ms.txt")
d6 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output_play/nd=false:mcs=0:spp=default/PointCloud1m:rate=15/QoS=volatile,reliable:DDS=rmw_cyclonedds_cpp/raqs=default:rate=default/jitter_ms.txt")
d7 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output_play/nd=false:mcs=0:spp=default/PointCloud2m:rate=15/QoS=volatile,reliable:DDS=rmw_cyclonedds_cpp/raqs=default:rate=default/jitter_ms.txt")
d8 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output_play/nd=false:mcs=0:spp=default/PointCloud4m:rate=15/QoS=volatile,reliable:DDS=rmw_cyclonedds_cpp/raqs=default:rate=default/jitter_ms.txt")

d1 = d1[10:1990, ]
d2 = d2[10:1990, ]
d3 = d3[10:1990, ]
d4 = d4[10:1990, ]
d5 = d5[10:1990, ]
d6 = d6[10:1990, ]
d7 = d7[10:1990, ]
d8 = d8[10:1990, ]

d1.dataframe = data.frame(data=d1,size=c(rep(xaxis_scale[1],length(d1))))
d2.dataframe = data.frame(data=d2,size=c(rep(xaxis_scale[2],length(d2))))
d3.dataframe = data.frame(data=d3,size=c(rep(xaxis_scale[3],length(d3))))
d4.dataframe = data.frame(data=d4,size=c(rep(xaxis_scale[4],length(d4))))
d5.dataframe = data.frame(data=d5,size=c(rep(xaxis_scale[5],length(d5))))
d6.dataframe = data.frame(data=d6,size=c(rep(xaxis_scale[6],length(d6))))
d7.dataframe = data.frame(data=d7,size=c(rep(xaxis_scale[7],length(d7))))
d8.dataframe = data.frame(data=d8,size=c(rep(xaxis_scale[8],length(d8))))


data1 = rbind(d1.dataframe,d2.dataframe,d3.dataframe,d4.dataframe,d5.dataframe,d6.dataframe,d7.dataframe,d8.dataframe) %>%
    transform(name=c(rep(v_label[1],length(d1)*8)))

d1 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output_play/nd=false:mcs=0:spp=default/RadarDetection:rate=15/QoS=volatile,reliable:DDS=rmw_cyclonedds_cpp/raqs=1048576:rate=default/jitter_ms.txt")
d2 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output_play/nd=false:mcs=0:spp=default/Range:rate=15/QoS=volatile,reliable:DDS=rmw_cyclonedds_cpp/raqs=1048576:rate=default/jitter_ms.txt")
d3 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output_play/nd=false:mcs=0:spp=default/NavSatFix:rate=15/QoS=volatile,reliable:DDS=rmw_cyclonedds_cpp/raqs=1048576:rate=default/jitter_ms.txt")
d4 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output_play/nd=false:mcs=0:spp=default/RadarTrack:rate=15/QoS=volatile,reliable:DDS=rmw_cyclonedds_cpp/raqs=1048576:rate=default/jitter_ms.txt")
d5 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output_play/nd=false:mcs=0:spp=default/PointCloud512k:rate=15/QoS=volatile,reliable:DDS=rmw_cyclonedds_cpp/raqs=1048576:rate=default/jitter_ms.txt")
d6 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output_play/nd=false:mcs=0:spp=default/PointCloud1m:rate=15/QoS=volatile,reliable:DDS=rmw_cyclonedds_cpp/raqs=1048576:rate=default/jitter_ms.txt")
d7 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output_play/nd=false:mcs=0:spp=default/PointCloud2m:rate=15/QoS=volatile,reliable:DDS=rmw_cyclonedds_cpp/raqs=1048576:rate=default/jitter_ms.txt")
d8 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output_play/nd=false:mcs=0:spp=default/PointCloud4m:rate=15/QoS=volatile,reliable:DDS=rmw_cyclonedds_cpp/raqs=1048576:rate=default/jitter_ms.txt")

d1 = d1[10:1990, ]
d2 = d2[10:1990, ]
d3 = d3[10:1990, ]
d4 = d4[10:1990, ]
d5 = d5[10:1990, ]
d6 = d6[10:1990, ]
d7 = d7[10:1990, ]
d8 = d8[10:1990, ]


d1.dataframe = data.frame(data=d1,size=c(rep(xaxis_scale[1],length(d1))))
d2.dataframe = data.frame(data=d2,size=c(rep(xaxis_scale[2],length(d2))))
d3.dataframe = data.frame(data=d3,size=c(rep(xaxis_scale[3],length(d3))))
d4.dataframe = data.frame(data=d4,size=c(rep(xaxis_scale[4],length(d4))))
d5.dataframe = data.frame(data=d5,size=c(rep(xaxis_scale[5],length(d5))))
d6.dataframe = data.frame(data=d6,size=c(rep(xaxis_scale[6],length(d6))))
d7.dataframe = data.frame(data=d7,size=c(rep(xaxis_scale[7],length(d7))))
d8.dataframe = data.frame(data=d8,size=c(rep(xaxis_scale[8],length(d8))))

data2 = rbind(d1.dataframe,d2.dataframe,d3.dataframe,d4.dataframe,d5.dataframe,d6.dataframe,d7.dataframe,d8.dataframe) %>%
    transform(name=c(rep(v_label[2],length(d1)*8)))

d1 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output_play/nd=false:mcs=0:spp=default/RadarDetection:rate=15/QoS=volatile,reliable:DDS=rmw_cyclonedds_cpp/raqs=10485760:rate=default/jitter_ms.txt")
d2 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output_play/nd=false:mcs=0:spp=default/Range:rate=15/QoS=volatile,reliable:DDS=rmw_cyclonedds_cpp/raqs=10485760:rate=default/jitter_ms.txt")
d3 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output_play/nd=false:mcs=0:spp=default/NavSatFix:rate=15/QoS=volatile,reliable:DDS=rmw_cyclonedds_cpp/raqs=10485760:rate=default/jitter_ms.txt")
d4 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output_play/nd=false:mcs=0:spp=default/RadarTrack:rate=15/QoS=volatile,reliable:DDS=rmw_cyclonedds_cpp/raqs=10485760:rate=default/jitter_ms.txt")
d5 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output_play/nd=false:mcs=0:spp=default/PointCloud512k:rate=15/QoS=volatile,reliable:DDS=rmw_cyclonedds_cpp/raqs=10485760:rate=default/jitter_ms.txt")
d6 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output_play/nd=false:mcs=0:spp=default/PointCloud1m:rate=15/QoS=volatile,reliable:DDS=rmw_cyclonedds_cpp/raqs=10485760:rate=default/jitter_ms.txt")
d7 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output_play/nd=false:mcs=0:spp=default/PointCloud2m:rate=15/QoS=volatile,reliable:DDS=rmw_cyclonedds_cpp/raqs=10485760:rate=default/jitter_ms.txt")
d8 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output_play/nd=false:mcs=0:spp=default/PointCloud4m:rate=15/QoS=volatile,reliable:DDS=rmw_cyclonedds_cpp/raqs=10485760:rate=default/jitter_ms.txt")

d1 = d1[10:1990, ]
d2 = d2[10:1990, ]
d3 = d3[10:1990, ]
d4 = d4[10:1990, ]
d5 = d5[10:1990, ]
d6 = d6[10:1990, ]
d7 = d7[10:1990, ]
d8 = d8[10:1990, ]


d1.dataframe = data.frame(data=d1,size=c(rep(xaxis_scale[1],length(d1))))
d2.dataframe = data.frame(data=d2,size=c(rep(xaxis_scale[2],length(d2))))
d3.dataframe = data.frame(data=d3,size=c(rep(xaxis_scale[3],length(d3))))
d4.dataframe = data.frame(data=d4,size=c(rep(xaxis_scale[4],length(d4))))
d5.dataframe = data.frame(data=d5,size=c(rep(xaxis_scale[5],length(d5))))
d6.dataframe = data.frame(data=d6,size=c(rep(xaxis_scale[6],length(d6))))
d7.dataframe = data.frame(data=d7,size=c(rep(xaxis_scale[7],length(d7))))
d8.dataframe = data.frame(data=d8,size=c(rep(xaxis_scale[8],length(d8))))


data3 = rbind(d1.dataframe,d2.dataframe,d3.dataframe,d4.dataframe,d5.dataframe,d6.dataframe,d7.dataframe,d8.dataframe) %>%
    transform(name=c(rep(v_label[3],length(d1)*8)))

d1 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output_play/nd=false:mcs=0:spp=default/RadarDetection:rate=15/QoS=volatile,reliable:DDS=rmw_cyclonedds_cpp/raqs=104857600:rate=default/jitter_ms.txt")
d2 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output_play/nd=false:mcs=0:spp=default/Range:rate=15/QoS=volatile,reliable:DDS=rmw_cyclonedds_cpp/raqs=104857600:rate=default/jitter_ms.txt")
d3 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output_play/nd=false:mcs=0:spp=default/NavSatFix:rate=15/QoS=volatile,reliable:DDS=rmw_cyclonedds_cpp/raqs=104857600:rate=default/jitter_ms.txt")
d4 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output_play/nd=false:mcs=0:spp=default/RadarTrack:rate=15/QoS=volatile,reliable:DDS=rmw_cyclonedds_cpp/raqs=104857600:rate=default/jitter_ms.txt")
d5 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output_play/nd=false:mcs=0:spp=default/PointCloud512k:rate=15/QoS=volatile,reliable:DDS=rmw_cyclonedds_cpp/raqs=104857600:rate=default/jitter_ms.txt")
d6 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output_play/nd=false:mcs=0:spp=default/PointCloud1m:rate=15/QoS=volatile,reliable:DDS=rmw_cyclonedds_cpp/raqs=104857600:rate=default/jitter_ms.txt")
d7 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output_play/nd=false:mcs=0:spp=default/PointCloud2m:rate=15/QoS=volatile,reliable:DDS=rmw_cyclonedds_cpp/raqs=104857600:rate=default/jitter_ms.txt")
d8 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output_play/nd=false:mcs=0:spp=default/PointCloud4m:rate=15/QoS=volatile,reliable:DDS=rmw_cyclonedds_cpp/raqs=104857600:rate=default/jitter_ms.txt")

d1 = d1[10:1990, ]
d2 = d2[10:1990, ]
d3 = d3[10:1990, ]
d4 = d4[10:1990, ]
d5 = d5[10:1990, ]
d6 = d6[10:1990, ]
d7 = d7[10:1990, ]
d8 = d8[10:1990, ]


d1.dataframe = data.frame(data=d1,size=c(rep(xaxis_scale[1],length(d1))))
d2.dataframe = data.frame(data=d2,size=c(rep(xaxis_scale[2],length(d2))))
d3.dataframe = data.frame(data=d3,size=c(rep(xaxis_scale[3],length(d3))))
d4.dataframe = data.frame(data=d4,size=c(rep(xaxis_scale[4],length(d4))))
d5.dataframe = data.frame(data=d5,size=c(rep(xaxis_scale[5],length(d5))))
d6.dataframe = data.frame(data=d6,size=c(rep(xaxis_scale[6],length(d6))))
d7.dataframe = data.frame(data=d7,size=c(rep(xaxis_scale[7],length(d7))))
d8.dataframe = data.frame(data=d8,size=c(rep(xaxis_scale[8],length(d8))))



data4 = rbind(d1.dataframe,d2.dataframe,d3.dataframe,d4.dataframe,d5.dataframe,d6.dataframe,d7.dataframe,d8.dataframe) %>%
    transform(name=c(rep(v_label[4],length(d1)*8)))


all_data = rbind(data1,data2,data3,data4) %>%
    mutate(size=factor(size,levels=xaxis_scale),name=factor(name,levels=v_label)) %>%
    na.omit()
#パイプ(%>%)を使用しない
# all_data = rbind(data1,data2,data3,data4)
# all_data = mutate(all_data,size=factor(size,levels=xaxis_scale))

ggp = all_data %>%
    ggplot(aes(x=factor(name),y=data,fill=factor(name)))+ #name,dataというカラムを表示する
    stat_boxplot(geom = "errorbar", width=0.4,coef=0.8) + #errorbar(端の横線)を表示
    geom_boxplot(outlier.colour=NA, na.rm=TRUE,coef=0.8)+ #箱ひげ図を表示
    #分割表示の設定
    facet_wrap(~size, ncol=11,strip.position = "bottom")+ #size(自分で設定したカラム名)で分割。ncolで横のカラム数の指定
    #y軸の設定
    scale_y_continuous(
        breaks=c(-2,-1,-0.1,0,0.1,1,2), #表示する目盛りを指定
        trans=pseudo_log_trans(sigma = 0.05, base = exp(1)), #logスケールにする。sigmaを小さくしてlogの傾きを大きくする
        name="Jitter [ms]",
        # limits=c(-0.7,0.7),
    )+
    #x軸の設定
    scale_x_discrete(
        label=NULL,
        name="Message type",
        breaks=NULL, #横軸の分割を消す
    )+
    #legendの設定
    scale_fill_manual(name=NULL,values=box_cols)+ #
    #全体の配置場所と大きさの設定
    theme(legend.position="top",text=element_text(size=30))+ #
    coord_cartesian(ylim = c(-2, 2))

plot(ggp)
ggsave("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/boxplot_log_for_iros/practical/pra_raqs_15.eps",width=25,height=9)
