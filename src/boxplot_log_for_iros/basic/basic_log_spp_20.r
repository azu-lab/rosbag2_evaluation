library(dplyr)
library(ggplot2)
library(scales)

xaxis_scale = c('Array_1KB','Array_4KB','Array_16KB','Array_32KB','Array_64KB','Array_256KB','Array_1MB','Array_2MB','Struct_256B','Struct_4KB','Struct_32KB')
v_label = c("default","resilient")
box_cols <- c("#f7f7f7", "#cccccc","#969696","#525252")                # box colors

d1 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output2/nd=false_mcs=default_spp=default/Array1k_rate=20/QoS=volatile,reliable_DDS=rmw_cyclonedds_cpp/jitter_ms.txt")
d2 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output2/nd=false_mcs=default_spp=default/Array4k_rate=20/QoS=volatile,reliable_DDS=rmw_cyclonedds_cpp/jitter_ms.txt")
d3 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output2/nd=false_mcs=default_spp=default/Array16k_rate=20/QoS=volatile,reliable_DDS=rmw_cyclonedds_cpp/jitter_ms.txt")
d4 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output2/nd=false_mcs=default_spp=default/Array32k_rate=20/QoS=volatile,reliable_DDS=rmw_cyclonedds_cpp/jitter_ms.txt")
d5 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output2/nd=false_mcs=default_spp=default/Array64k_rate=20/QoS=volatile,reliable_DDS=rmw_cyclonedds_cpp/jitter_ms.txt")
d6 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output2/nd=false_mcs=default_spp=default/Array256k_rate=20/QoS=volatile,reliable_DDS=rmw_cyclonedds_cpp/jitter_ms.txt")
d7 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output2/nd=false_mcs=default_spp=default/Array1m_rate=20/QoS=volatile,reliable_DDS=rmw_cyclonedds_cpp/jitter_ms.txt")
d8 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output2/nd=false_mcs=default_spp=default/Array2m_rate=20/QoS=volatile,reliable_DDS=rmw_cyclonedds_cpp/jitter_ms.txt")
d9 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output2/nd=false_mcs=default_spp=default/Struct256_rate=20/QoS=volatile,reliable_DDS=rmw_cyclonedds_cpp/jitter_ms.txt")
d10 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output2/nd=false_mcs=default_spp=default/Struct4k_rate=20/QoS=volatile,reliable_DDS=rmw_cyclonedds_cpp/jitter_ms.txt")
d11 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output2/nd=false_mcs=default_spp=default/Struct32k_rate=20/QoS=volatile,reliable_DDS=rmw_cyclonedds_cpp/jitter_ms.txt")

d1 = d1[10:1990, ]
d2 = d2[10:1990, ]
d3 = d3[10:1990, ]
d4 = d4[10:1990, ]
d5 = d5[10:1990, ]
d6 = d6[10:1990, ]
d7 = d7[10:1990, ]
d8 = d8[10:1990, ]
d9 = d9[10:1990, ]
d10 = d10[10:1990, ]
d11 = d11[10:1990, ]

d1.dataframe = data.frame(data=d1,size=c(rep(xaxis_scale[1],length(d1))))
d2.dataframe = data.frame(data=d2,size=c(rep(xaxis_scale[2],length(d2))))
d3.dataframe = data.frame(data=d3,size=c(rep(xaxis_scale[3],length(d3))))
d4.dataframe = data.frame(data=d4,size=c(rep(xaxis_scale[4],length(d4))))
d5.dataframe = data.frame(data=d5,size=c(rep(xaxis_scale[5],length(d5))))
d6.dataframe = data.frame(data=d6,size=c(rep(xaxis_scale[6],length(d6))))
d7.dataframe = data.frame(data=d7,size=c(rep(xaxis_scale[7],length(d7))))
d8.dataframe = data.frame(data=d8,size=c(rep(xaxis_scale[8],length(d8))))
d9.dataframe = data.frame(data=d9,size=c(rep(xaxis_scale[9],length(d9))))
d10.dataframe = data.frame(data=d10,size=c(rep(xaxis_scale[10],length(d10))))
d11.dataframe = data.frame(data=d11,size=c(rep(xaxis_scale[11],length(d11))))

data1 = rbind(d1.dataframe,d2.dataframe,d3.dataframe,d4.dataframe,d5.dataframe,d6.dataframe,d7.dataframe,d8.dataframe,d9.dataframe,d10.dataframe,d11.dataframe) %>%
    transform(name=c(rep(v_label[1],length(d1)*11)))

d1 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output2/nd=false_mcs=default_spp=resilient/Array1k_rate=20/QoS=volatile,reliable_DDS=rmw_cyclonedds_cpp/jitter_ms.txt")
d2 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output2/nd=false_mcs=default_spp=resilient/Array4k_rate=20/QoS=volatile,reliable_DDS=rmw_cyclonedds_cpp/jitter_ms.txt")
d3 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output2/nd=false_mcs=default_spp=resilient/Array16k_rate=20/QoS=volatile,reliable_DDS=rmw_cyclonedds_cpp/jitter_ms.txt")
d4 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output2/nd=false_mcs=default_spp=resilient/Array32k_rate=20/QoS=volatile,reliable_DDS=rmw_cyclonedds_cpp/jitter_ms.txt")
d5 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output2/nd=false_mcs=default_spp=resilient/Array64k_rate=20/QoS=volatile,reliable_DDS=rmw_cyclonedds_cpp/jitter_ms.txt")
d6 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output2/nd=false_mcs=default_spp=resilient/Array256k_rate=20/QoS=volatile,reliable_DDS=rmw_cyclonedds_cpp/jitter_ms.txt")
d7 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output2/nd=false_mcs=default_spp=resilient/Array1m_rate=20/QoS=volatile,reliable_DDS=rmw_cyclonedds_cpp/jitter_ms.txt")
d8 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output2/nd=false_mcs=default_spp=resilient/Array2m_rate=20/QoS=volatile,reliable_DDS=rmw_cyclonedds_cpp/jitter_ms.txt")
d9 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output2/nd=false_mcs=default_spp=resilient/Struct256_rate=20/QoS=volatile,reliable_DDS=rmw_cyclonedds_cpp/jitter_ms.txt")
d10 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output2/nd=false_mcs=default_spp=resilient/Struct4k_rate=20/QoS=volatile,reliable_DDS=rmw_cyclonedds_cpp/jitter_ms.txt")
d11 = read.table("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/time_output2/nd=false_mcs=default_spp=resilient/Struct32k_rate=20/QoS=volatile,reliable_DDS=rmw_cyclonedds_cpp/jitter_ms.txt")

d1 = d1[10:1990, ]
d2 = d2[10:1990, ]
d3 = d3[10:1990, ]
d4 = d4[10:1990, ]
d5 = d5[10:1990, ]
d6 = d6[10:1990, ]
d7 = d7[10:1990, ]
d8 = d8[10:1990, ]
d9 = d9[10:1990, ]
d10 = d10[10:1990, ]
d11 = d11[10:1990, ]

d1.dataframe = data.frame(data=d1,size=c(rep(xaxis_scale[1],length(d1))))
d2.dataframe = data.frame(data=d2,size=c(rep(xaxis_scale[2],length(d2))))
d3.dataframe = data.frame(data=d3,size=c(rep(xaxis_scale[3],length(d3))))
d4.dataframe = data.frame(data=d4,size=c(rep(xaxis_scale[4],length(d4))))
d5.dataframe = data.frame(data=d5,size=c(rep(xaxis_scale[5],length(d5))))
d6.dataframe = data.frame(data=d6,size=c(rep(xaxis_scale[6],length(d6))))
d7.dataframe = data.frame(data=d7,size=c(rep(xaxis_scale[7],length(d7))))
d8.dataframe = data.frame(data=d8,size=c(rep(xaxis_scale[8],length(d8))))
d9.dataframe = data.frame(data=d9,size=c(rep(xaxis_scale[9],length(d9))))
d10.dataframe = data.frame(data=d10,size=c(rep(xaxis_scale[10],length(d10))))
d11.dataframe = data.frame(data=d11,size=c(rep(xaxis_scale[11],length(d11))))

data2 = rbind(d1.dataframe,d2.dataframe,d3.dataframe,d4.dataframe,d5.dataframe,d6.dataframe,d7.dataframe,d8.dataframe,d9.dataframe,d10.dataframe,d11.dataframe) %>%
    transform(name=c(rep(v_label[2],length(d1)*11)))


all_data = rbind(data1,data2) %>%
    mutate(size=factor(size,levels=xaxis_scale),name=factor(name,levels=v_label)) %>%
    na.omit()

ggp = all_data %>%
    ggplot(aes(x=factor(name),y=data,fill=factor(name)))+ #Display columns, name and data
    stat_boxplot(geom = "errorbar", width=0.4,coef=1) + #Display errorbar (horizontal line at the edge)
    geom_boxplot(outlier.colour=NA, na.rm=TRUE,coef=1)+ #Display box-plot
    ##Split display settings
    facet_wrap(~size, ncol=11,strip.position = "bottom")+ #Split by size. Specify the number of horizontal columns by ncol.
    #y-axis
    scale_y_continuous(
        breaks=c(-2,-1.0,-0.1,0,0.1,1.0,2.0), #Specify the scale to display
        trans=pseudo_log_trans(sigma = 0.05, base = exp(1)), #Decrease sigma and increase log slope.
        name="Jitter [ms]",
        # limits=c(-0.7,0.7),
    )+
    #x-axis
    scale_x_discrete(
        label=NULL,
        name="Message type",
        breaks=NULL, #Erase horizontal axis split
    )+
    #legend
    scale_fill_manual(name=NULL,values=box_cols)+ #
    #Overall placement location and size
    theme(legend.position="top",text=element_text(size=30))+ #
    coord_cartesian(ylim = c(-2.2, 2.2))

plot(ggp)
ggsave("/home/ryuko/perf_test_ws/src/performance_test/performance_test/helper_scripts/boxplot_log_for_iros/basic/basic_spp_20.eps",width=25,height=9)
