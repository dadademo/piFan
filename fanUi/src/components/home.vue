<template>
  <div>
    <div class="temp-ecahrs">
      <van-field
        v-model="filterTimeText"
        is-link
        readonly
        label="时间"
        placeholder="请选择时间"
        @click="showPicker = true"
      />

      <div class="temp-ecahrs-info" ref="ecahrs"></div>
    </div>
    <!-- <div class="ctrl-item-body">
      <div class="ctrl-item ctrl-item-row">20℃</div>
    </div> -->

    <div class="ctrl-item-body">
      <div class="ctrl-item">
        <div style="height: 10vh">{{ setTemp }}</div>
        <van-slider class="item-slider" v-model="setTemp"> </van-slider>
      </div>
      <div class="ctrl-item" @click="handleCtrlFan({ setTemp })">设定</div>
    </div>

    <div class="ctrl-item-body">
      <div
        class="ctrl-item ctrl-item-row"
        @click="handleCtrlFan({ fanStatus: 1 })"
      >
        开
      </div>
    </div>
    <div class="ctrl-item-body">
      <div
        class="ctrl-item ctrl-item-row"
        @click="handleCtrlFan({ fanStatus: 0 })"
      >
        关
      </div>
    </div>

    <van-popup v-model:show="showPicker" round position="bottom">
      <van-picker
        :columns="timeOptions"
        @cancel="showPicker = false"
        @confirm="onConfirm"
      />
    </van-popup>
  </div>
</template>

<script>
import { Slider, Field, Popup, Picker } from "vant";
import * as echarts from "echarts";
import moment from "moment";
import { getFanInfo, getLastData, setFanInfo } from "@/api/fan.js";
export default {
  name: "homeComp",
  components: {
    [Slider.name]: Slider,
    [Field.name]: Field,
    [Popup.name]: Popup,
    [Picker.name]: Picker,
  },
  data() {
    return {
      showPicker: false,
      filterTimeText: "本天",
      setTemp: 0,
      timeQuery: "day",
      timeOptions: [
        { text: "本天", value: "day" },
        { text: "近一周", value: "week" },
        { text: "本月", value: "month" },
      ],
      tempList: [],
    };
  },
  mounted() {
    this.initData();
    this.initLastInfo();
  },
  methods: {
    initData() {
      let query = { all: true };
      if (this.timeQuery === "week" || this.timeQuery === "month") {
        query.startTimestamp = moment()
          .subtract({ week: 7, month: 31 }[this.timeQuery], "days")
          .startOf("day")
          .valueOf();
        query.endTimestamp = moment().endOf("day").valueOf();
      } else if (this.timeQuery === "day") {
        query.startTimestamp = moment().startOf(this.timeQuery).valueOf();
        query.endTimestamp = moment().endOf(this.timeQuery).valueOf();
      }
      getFanInfo(query).then((list) => {
        this.tempList = list.map((item) => ({
          ...item,
          timeFormat: moment(item.time).format("YYYY-MM-DD HH:mm:ss"),
        }));
        this.initLine();
      });
    },
    initLastInfo() {
      getLastData().then((info) => {
        this.setTemp = info.setTemp;
      });
    },
    onConfirm({ selectedOptions }) {
      this.showPicker = false;
      this.filterTimeText = selectedOptions[0].text;
    },
    initLine() {
      var chartDom = this.$refs.ecahrs;
      var myChart = echarts.init(chartDom);
      const option = {
        tooltip: {
          trigger: "axis",
        },
        legend: {
          top: "3%",
          data: ["温度", "开关"],
        },
        grid: {
          left: "10%",
          right: "10%",
          bottom: "10%",
          top: "10%",
        },
        // toolbox: {
        //   feature: {
        //     saveAsImage: {},
        //   },
        // },
        xAxis: {
          type: "category",
          boundaryGap: false,
          data: this.tempList.map((item) => item.timeFormat),
        },
        yAxis: [
          {
            type: "value",
            position: "left",
          },
          {
            name: "开关",
            type: "value",
            position: "right",
          },
        ],
        series: [
          {
            name: "温度",
            type: "line",
            smooth: true,
            areaStyle: {},
            emphasis: {
              focus: "series",
            },
            data: this.tempList.map((item) => item.temp),
            yAxisIndex: 0,
          },
          {
            name: "开关",
            type: "line",
            // stack: "Total",
            // smooth: true,
            areaStyle: {},
            emphasis: {
              focus: "series",
            },
            data: this.tempList.map((item) => item.fanStatus),
            yAxisIndex: 1,
          },
          {
            name: "设定",
            type: "line",
            // stack: "Total",
            // smooth: true,
            areaStyle: {},
            emphasis: {
              focus: "series",
            },
            data: this.tempList.map((item) => item.setTemp),
            yAxisIndex: 0,
          },
        ],
      };
      myChart.setOption(option);
    },
    handleCtrlFan(info) {
      setFanInfo(info).then(() => {
        this.initData();
        this.initLastInfo();
      });
    },
  },
};
</script>

<style scoped>
.temp-ecahrs {
  border-radius: 12px;
  width: calc(100vw - 40px);
  background-color: white;
  height: 50vh;
  margin: 10px auto 0 auto;
  padding: 10px;
}
.ctrl-item-body {
  display: flex;
  flex-wrap: wrap;
  border-radius: 12px;
  width: calc(100vw - 20px);
  background-color: white;
  margin: 10px auto 0 auto;
}
.ctrl-item {
  width: calc(50% - 1px);
  height: 12vh;
  font-size: 20px;
  text-align: center;
  line-height: 12vh;
}
.input-style {
  border: 0px solid black;
  width: 150px;
  height: 100%;
  text-align: center;
  font-size: 40px;
  padding: 0;
  margin: 0;
  border-radius: 12px;
}
.ctrl-item:not(:last-child) {
  border-right: 1px solid #d7dae2;
}
.ctrl-item-row {
  flex: 1;
}
.item-slider {
  width: 40vw;
  margin: 0 auto;
}
.temp-ecahrs-info {
  height: calc(50vh - 50px);
}
</style>