<template>
  <div class="guideContent">
    <div>
      <div class="bodyHeight justifyVerticalCenter">
        <img class="arrowHeight" src="../assets/leftArrow.png" alt="" v-if="status != 0" @click="moveToBefore()" />
      </div>
      <div class="dummyMargin2 arrowHeight"></div>
    </div>
    <div class="contentBody">
      <div class="bodyHeight justifyCenter">
        <img v-if="status == 0" class="bodyImage" src="../assets/train1.png" alt="" />
        <img v-if="status == 1" class="bodyImage" src="../assets/train2.png" alt="" />
        <img v-if="status == 2" class="bodyImage" src="../assets/train3.png" alt="" />
        <img v-if="status == 3" class="bodyImage" src="../assets/train4.png" alt="" />
      </div>
      <div class="textStyle">
        <div v-if="status == 0">
          <div>(1) 메뉴에서 "다른 파일 열기"를 선택하여 (2) 학습할 Data Set과 학습 모델 저장 위치를 선택합니다.</div>
          <br />
          <div>양품과 불량을 구분하여 Train Data 파일 경로를 선택합니다.</div>
          <br />
          <div>Test Data, Validation Data가 별도로 있는 경우 파일을 선택하며, 별도 선택이 없으면 설정한 비율에 맞게 이미지가 자동으로 할당됩니다.</div>
          <br />
          <div>※ jpg, png 형식 외의 파일은 학습이 불가능 합니다.</div>
        </div>
        <div v-if="status == 1">
          <div>(1) Augmentation 여부와 Hyperparameter 을 조절합니다.</div>
          <br />
          <div>Augmentation의 4가지 기능 중 원하는 것만을 적용합니다.</div>
          <br />
          <div>Hyperparameter는 Epoch, Learning Rate, Batch Size, Decay Step 4가지 기능을 원하는 수치로 조정합니다.</div>
          <br />
          <div>Epoch를 제외한 3가지 항목은 일반적으로 자주 쓰이는 수치를 제공합니다.</div>
        </div>
        <div v-if="status == 2">
          <div>(1) 제어단의 "시작", "정지" 버튼으로 학습을 진행합니다.</div>
          <br />
          <div>그래프와 로그, 프로그래프바를 통해 진행 상황을 파악합니다.</div>
          <br />
          <div>학습 정지 시 해당 순간의 모델이 저장되며, 이어서 학습할 수 없습니다.</div>
        </div>
        <div v-if="status == 3">
          <div>학습 완료 후, 초기에 설정한 저장 위치에 해당 날짜 이름의 폴더가 생깁니다.</div>
          <br />
          <div>폴더 내부에 학습 모델과 로그 파일이 저장됩니다.</div>
          <br />
          <div>학습 모델은 ONNX 형식, 로그는 log 형식으로 저장됩니다.</div>
        </div>
      </div>
    </div>
    <div>
      <div class="bodyHeight justifyVerticalCenter">
        <img class="arrowHeight" src="../assets/rightArrow.png" alt="" v-if="status != 3" @click="moveToNext()" />
      </div>
      <div class="dummyMargin2 arrowHeight"></div>
    </div>
    <!-- <div>rigthArrow</div> -->
  </div>
</template>

<script>
export default {
  data() {
    return {
      status: 0,
      index: 0,
      images: ["train1", "train2", "train3", "train4"],
    };
  },
  methods: {
    moveToBefore() {
      if (this.status < 4) this.status = this.status - 1;
    },
    moveToNext() {
      if (this.status >= 0) this.status = this.status + 1;
    },
  },
};
</script>

<style scoped>
.guideContent {
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  /* padding: 20rem 0; */
  /* border: 1px #000000 solid; */
  height: 50rem;
  width: 100%;
}
.bodyHeight {
  height: 70%;
}
.justifyVerticalCenter {
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 30%;
}
.arrowHeight {
  /* height: 10%; */
  width: 100%;
}
.dummyMargin2 {
  width: 5rem;
}
.contentBody {
  width: 60%;
  /* background-color: rgb(201, 204, 215); */
}
.justifyCenter {
  display: flex;
  justify-content: center;
  align-items: center;
}
.bodyImage {
  height: 80%;
  /* width: 80%; */
  box-shadow: 0 0 12px 2px #b6b6b6;
}
.textStyle {
  padding: 1rem 2rem;
  font-size: 1.1em;
  text-align: left;
  /* box-shadow: 0 0 30px 1px #dcdcdc66; */
}
</style>
