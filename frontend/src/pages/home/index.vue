<template>
  <div class="mx-auto container py-4 grid grid-cols-1 lg:grid-cols-2 gap-5 md:gap-2 lg:gap-5 min-h-screen" v-if="!isLoading">
    <div class="flex flex-col gap-6">
      <h1 class="font-bold text-2xl">Tổng quan Dataset</h1>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="flex justify-between align-middle items-center p-4 rounded-xl bg-gray-200">
          <p class="font-bold">Số lượng đặc trưng</p>
          <p>{{ overall_info.number_of_feature }}</p>
        </div>
        <div class="flex justify-between align-middle items-center p-4 rounded-xl bg-gray-200">
          <p class="font-bold">Tổng số bảng ghi</p>
          <p>{{ overall_info.number_of_sample }}</p>
        </div>
        <div class="flex justify-between align-middle items-center p-4 rounded-xl bg-gray-200">
          <p class="font-bold">Số lượng bảng ghi huấn luyện</p>
          <p>{{ overall_info.training_sample }}</p>
        </div>
        <div class="flex justify-between align-middle items-center p-4 rounded-xl bg-gray-200">
          <p class="font-bold">Số lượng bảng ghi kiểm thử</p>
          <p>{{ overall_info.testing_sample }}</p>
        </div>
      </div>
      <hr>
      <h1 class="font-bold text-2xl">Các mô hình đã huấn luyện</h1>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div v-for="model in all_model"  :key="model" class="p-4 rounded-xl bg-red-100">
          <div  class="flex justify-between align-middle items-center ">
            <p class="font-bold">Tên mô hình</p>
            <p>{{ model.name}}</p>
          </div>
        </div>
      </div>
      <hr>
      <div class="flex justify-between">
        <h1 class="font-bold text-2xl">Dữ liệu ngẫu nhiên chưa phân loại</h1>
        <button @click="get_non_label_dataset" class="btn btn-square hover:rotate-90">
          <svg xmlns="http://www.w3.org/2000/svg" height="16" width="16" viewBox="0 0 512 512"><path d="M142.9 142.9c62.2-62.2 162.7-62.5 225.3-1L327 183c-6.9 6.9-8.9 17.2-5.2 26.2s12.5 14.8 22.2 14.8H463.5c0 0 0 0 0 0H472c13.3 0 24-10.7 24-24V72c0-9.7-5.8-18.5-14.8-22.2s-19.3-1.7-26.2 5.2L413.4 96.6c-87.6-86.5-228.7-86.2-315.8 1C73.2 122 55.6 150.7 44.8 181.4c-5.9 16.7 2.9 34.9 19.5 40.8s34.9-2.9 40.8-19.5c7.7-21.8 20.2-42.3 37.8-59.8zM16 312v7.6 .7V440c0 9.7 5.8 18.5 14.8 22.2s19.3 1.7 26.2-5.2l41.6-41.6c87.6 86.5 228.7 86.2 315.8-1c24.4-24.4 42.1-53.1 52.9-83.7c5.9-16.7-2.9-34.9-19.5-40.8s-34.9 2.9-40.8 19.5c-7.7 21.8-20.2 42.3-37.8 59.8c-62.2 62.2-162.7 62.5-225.3 1L185 329c6.9-6.9 8.9-17.2 5.2-26.2s-12.5-14.8-22.2-14.8H48.4h-.7H40c-13.3 0-24 10.7-24 24z"/></svg>
        </button>
      </div>
      <div class="grid grid-cols-2 md:grid-cols-5 gap-4 pb-1">
        <div v-for="(data, index) in non_label_dataset" @click="parseEntry(data.content)" :key="index" class="p-4 rounded-xl bg-yellow-100 cursor-pointer">
          <div class="flex flex-col justify-between align-middle items-center overflow-hidden">
            <p class="font-bold">Dữ liệu {{ index+1 }}</p>
            <p class="line-clamp-3 text-sm text-left font-mono">{{ data.content }}</p>
            <p>(Xem thêm)</p>
          </div>
        </div>
      </div>
    </div>

    <div class="flex flex-col gap-4 lg:pl-4">
      <h1 class="font-bold text-2xl">Gợi ý khóa học</h1>
      <div class="grid grid-cols-1 gap-3">
        <label class="form-control w-full">
          <div class="label">
            <span class="label-text">Mong muốn của bạn đối với khóa học</span>
          </div>
          <textarea placeholder="Bio" v-model="entry.check_text" class="textarea textarea-bordered textarea-lg min-h-[200px] w-full" ></textarea>
        </label>
        </div>
        <button @click="predictNow" class="btn btn-wide mx-auto">Dự đoán ngay</button>
    </div>
    <input type="checkbox" hidden id="my_modal" class="modal-toggle"  />
    <div class="modal" role="dialog">
      <div class="modal-box max-w-fit">
        <div class="flex justify-between">
          <h3 class="text-lg font-bold">Thống kê dự đoán của các mô hình</h3>
          <p class="text-lg font-bold"><span v-show="predictions.length>0">Kết quả tối ưu: {{ bestChoice }}</span></p>
        </div>
        <div v-if="predictions.length > 0">
          <div class="grid grid-cols-4 gap-4 mt-4">
            <div v-for="prediction in predictions" :key="prediction.name" class="p-4 rounded-xl bg-blue-50 shadow-lg">
              <div  class="flex justify-between align-middle items-center gap-4">
                <p class="font-bold">Tên mô hình</p>
                <p>{{ prediction.name.replace("OvO", " - OneVsOne").replace("OvA", " - OneVsAll") }}</p>
              </div>
              <div  class="flex justify-between align-middle items-center gap-4">
                <p class="font-bold">Kết quả dự đoán</p>
                <p class="font-semibold">{{ prediction.prediction }}</p>
              </div>
            </div>
          </div>
          <h3 class="text-xl text-center font-bold mt-8">Gợi ý các khóa học cho bạn</h3>
          <div class="grid grid-cols-1 gap-4 mt-4">
            <Flicking ref="flicking" 
              :options="flickingOptions"
              :viewportTag="'div'"
              :cameraTag="'div'"
              :cameraClass="''"
              :plugins="plugins"
              @move-end="onMoveEnd"
              class="text-white font-bold text-3xl capitalize pb-10">
              <div v-for="course in recomDict" :key="course.title" class="relative panel w-full shadow-md shadow-yellow-100 h-full bg-black text-white p-4 rounded-lg font-normal">
                <p class="text-lg font-bold text-center">{{ course.title }}</p>
                <p class="my-1 text-base text-center">{{ course.average_rating }}⭐/{{ course.review_count }} đánh giá</p>
                <hr class="my-2">
                <p class="text-sm line-clamp-4 mb-2">{{ course.describe }}</p>
                <p class="text-base"><b>Kỹ năng</b>: {{ course.skill }}</p>
                <p class="text-base"><b>Số lượng học viên</b>: {{ course.students_enrolled }}</p>
                <div v-show="course.best_seller" class="absolute top-1 left-1 hover:bg-white p-1 rounded-md text-sm group flex gap-2">❤️<span class="hidden group-hover:block text-black font-semibold">được yêu thích</span></div>
              </div>
              <template #viewport>
                <div class="flicking-pagination"></div>
                <span class="flicking-arrow-prev"></span>
                <span class="flicking-arrow-next"></span>
              </template>
            </Flicking>
          </div>
        </div>
        <div v-else class="flex flex-col justify-center items-center mt-4">
          <div class="flex items-center justify-center">
            <div class="relative">
              <div class="h-16 w-16 rounded-full border-t-8 border-b-8 border-gray-200"></div>
              <div class="absolute top-0 left-0 h-16 w-16 rounded-full border-t-8 border-b-8 border-blue-500 animate-spin">
              </div>
            </div>
          </div>
          <h1 class="font-bold text-lg">Vui lòng chờ trong giây lát...</h1>
        </div>
      </div>
      <label class="modal-backdrop" for="my_modal">Close</label>
    </div>
  </div>
  <div v-else class="flex items-center justify-center h-screen">
    <div class="relative">
        <div class="h-24 w-24 rounded-full border-t-8 border-b-8 border-gray-200"></div>
        <div class="absolute top-0 left-0 h-24 w-24 rounded-full border-t-8 border-b-8 border-blue-500 animate-spin">
        </div>
    </div>
  </div>
</template>

<script>
import { useExampleStore } from '@/stores/examStore'
import axios from 'axios';
import Flicking from "@egjs/vue3-flicking";
import { Fade, AutoPlay, Pagination, Perspective, Arrow } from "@egjs/flicking-plugins";
import "@egjs/flicking-plugins/dist/pagination.css";
import "@egjs/flicking-plugins/dist/arrow.css";

const api_url = "http://localhost:8000/api/"

export default {
  name: "home-page",
  components: {
    Flicking,
  },
  setup() {
    const store = useExampleStore()
    const flickingOptions = { 
      circular: true,
      panelsPerView: 7
    }
    const plugins = [
      new Perspective({ rotate: -1, scale: 3, perspective: 300 }),
      new Pagination({  type: 'scroll' }),
      new Fade(),
      new Arrow(),
      new AutoPlay({ duration: 1000, direction: "NEXT", stopOnHover: false })
    ]
    return {
      store, flickingOptions, plugins
    }
  },
  data(){
    return {
      entry: {
        'check_text': null,
      },
      "predictions": [],
      "recomDict": [],
      "overall_info": {
        "number_of_feature": "",
        "number_of_sample": "",
        "testing_sample": "",
        "training_sample": ""
      },
      "all_model": [],
      "non_label_dataset": [],
      "isLoading": true
    }
  },
  methods: {
    parseEntry(data) {
      this.entry.check_text = data
    },
    predictNow() {
      for (let key in this.entry) {
        if (key in this.entry) {
          if (this.entry[key] == null) {
            this.$swal('Vui lòng điền đầy đủ thông tin', '', "error");
            return
          }
        }
      }
      this.predictions = []
      this.recomDict = []
      this.bestChoice = ""
      document.getElementById('my_modal').click()
      axios.post(api_url + "predict", this.entry, {timeout: 60000})
        .then(response => {
          this.predictions =  response.data.entries
          this.bestChoice = response.data.best_choice
          this.recomDict = response.data.recom_dict
          this.entry.check_text = null
        })
        .catch(error => {
          console.error(error);
        });
    },
    get_overall_info() {
      axios.get(api_url + "info", {timeout: 60000})
        .then(response => {
          this.overall_info = response.data
        })
        .catch(error => {
          console.error(error);
        });
    },
    get_all_model() {
      axios.get(api_url + "model", {timeout: 60000})
        .then(response => {
          this.all_model = response.data.entries
        })
        .catch(error => {
          console.error(error);
        });
    },
    get_non_label_dataset() {
      axios.get(api_url + "raw-data", {timeout: 60000})
        .then(response => {
          this.non_label_dataset = response.data.entries
          this.isLoading = false
        })
        .catch(error => {
          console.error(error);
        });
    }
  },
  async created() {
    await this.get_overall_info()
    await this.get_all_model()
    this.get_non_label_dataset()
  }
};
</script>