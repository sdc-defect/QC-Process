<!-- <template>
  <mainLanding></mainLanding>
</template>

<script>
import mainLanding from "./views/landing.vue";
export default {
  name: "App",
  components: { mainLanding },
};
</script>

<style scoped></style> -->

<template>
  <div class="headerDisplay">
    <img src="./assets/logo.png" alt="" class="logoImg" />
    <div class="rightAlign">사용가이드</div>
  </div>
  <div class="topBackground" style="display: flex; flex-direction: column">
    <!-- <div>학습 프로그램</div>
    <div>추론 프로그램</div> -->
    <div class="btnDisplay">
      <button class="btnSingle fontNormal" @click="downloadTraining">학습 프로그램 <span class="material-symbols-outlined"> download </span></button>
      <button class="btnSingle fontNormal" @click="downloadInference">추론 프로그램 <span class="material-symbols-outlined"> download </span></button>
    </div>
  </div>
  <div class="title">
    <h2 class="fontBold">사용 가이드</h2>
  </div>
  <div class="horizontalAlign">
    <div @click="showTraining">
      <h2 :class="[status == 0 ? 'fontBold' : 'fontNormal']">학습 프로그램</h2>
    </div>
    <div @click="showInference">
      <h2 :class="[status == 1 ? 'fontBold' : 'fontNormal']">추론 프로그램</h2>
    </div>
  </div>
  <hr />
  <!-- <div class="dummyMargin1"></div> -->
  <div class="bodyContent">
    <div v-if="status == 0">
      <TrainingComponent></TrainingComponent>
    </div>
    <div v-if="status == 1">
      <InferenceComponent></InferenceComponent>
    </div>
  </div>
  <!-- <hr /> -->
  <div class="footerBody footerDisplay">
    <div class="footerMarginRight">
      <div>상호</div>
      <div>대표자</div>
      <div>전화번호</div>
      <div>메일</div>
      <div>주소</div>
    </div>
    <div class="footerMarginRight">
      <div>말해 Yes or No</div>
      <div>고 승효</div>
      <div>010-9536-1403</div>
      <div>tellYesOrNoPJT@gmail.com</div>
      <div>대전 광역시 유성구 덕명동 삼성화재연수원</div>
    </div>
    <!-- <div>
      <div>상호 : 말해 Yes or No</div>
      <div>대표자 : 고 승효</div>
      <div>전화번호: 010-9536-1403</div>
      <div>메일 : tellYesOrNoPJT@gmail.com</div>
      <div>주소 : 대전 광역시 유성구 덕명동 삼성화재연수원</div>
    </div> -->
  </div>
  <HelloWorld msg="Vite + Vue" />
</template>

<script>
import TrainingComponent from "./components/Training.vue";
import InferenceComponent from "./components/Inference.vue";
export default {
  components: { TrainingComponent, InferenceComponent },
  data() {
    return {
      status: 0, //0은 training, 1은 inference
    };
  },
  methods: {
    showTraining() {
      this.status = 0;
      console.log(this.status);
    },
    showInference() {
      this.status = 1;
      console.log(this.status);
    },
    downloadTraining() {
      window.open("https://drive.google.com/file/d/1iMNtSGJVIAveHiylGz1mqao2MdV9ZsfG/view?usp=sharing");
    },
    downloadInference() {
      window.open("https://drive.google.com/file/d/1iMNtSGJVIAveHiylGz1mqao2MdV9ZsfG/view?usp=sharing");
    },
  },
};
</script>

<style scoped>
.headerDisplay {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}
.logoImg {
  /* height: 80%; */
  margin: 0 2rem;
}
.topBackground {
  background-image: url("./assets/mainbg.png");
  background-size: cover;
  width: 100vw;
  height: 60vh;
  display: flex;
  justify-content: flex-end;
  align-items: flex-end;
  /* margin-top: 4rem; */
}
.rightAlign {
  text-align: right;
  margin: 1.3rem 3rem;
  font-size: 1.3em;
}
.title {
  margin-top: 5rem;
  margin-bottom: 3rem;
  font-size: 1.5em;
}
.horizontalAlign {
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
}
.dummyMargin1 {
  height: 3rem;
  /* background-color: aquamarine; */
}
.bodyImage {
  height: 80%;
  /* width: 80%; */
}
.footerBody {
  padding: 3rem;
  background-color: #33343e;
  color: #ffffff;
  text-align: left;
}
.footerDisplay {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
}
.footerMarginRight > div {
  margin-top: 0.3rem;
}
.footerMarginRight {
  margin-right: 2rem;
}
.bodyContent {
  /* height: 30vh; */
}
.btnDisplay {
  display: flex;
  flex-direction: row;
  margin-right: 1rem;
  /* background-color: aqua; */
  /* margin: 2rem; */
}
.btnSingle {
  margin-right: 1rem;
  margin-bottom: 1rem;
  background-color: #00000083;
  font-size: 1.2em;
  color: #ffffff;
  border-radius: 5px;
  border-width: 0;
  text-align: center;
  display: flex;
  align-items: center;
  box-shadow: 0 0 20px 2px #f9f9f9af;
}
.btnSingle:hover {
  background-color: rgb(0, 0, 0);
  color: #ffffff;
  border-width: 0;
}
.fontBold {
  font-family: "notoSansBold";
}
.fontNormal {
  font-family: "notoSans";
}
.fontNormal:hover {
  font-family: "notoSansBold";
}
/* .logo {
    height: 6em;
    padding: 1.5em;
    will-change: filter;
  }
  .logo:hover {
    filter: drop-shadow(0 0 2em #646cffaa);
  }
  .logo.vue:hover {
    filter: drop-shadow(0 0 2em #42b883aa);
  } */
</style>

