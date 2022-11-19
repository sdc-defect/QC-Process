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
        <img v-if="status == 0" class="bodyImage" src="../assets/inference1.png" alt="" />
        <img v-if="status == 1" class="bodyImage" src="../assets/inference2.png" alt="" />
        <img v-if="status == 2" class="bodyImage" src="../assets/inference3.png" alt="" />
        <img v-if="status == 3" class="bodyImage" src="../assets/inference4.png" alt="" />
      </div>
      <div class="textStyle">
        <div v-if="status == 0">
          <div>(1) 추론 결과가 저장될 로그 저장 경로를 설정합니다.</div>
          <br />
          <div>사용할 모델을 선택하고 모델을 서버에 업로드합니다.</div>
          <br />
          <div>추론 후, 지정한 로그 저장 경로에 추론 결과 이미지와 로그 파일이 저장됩니다.</div>
        </div>
        <div v-if="status == 1">
          <div>하나의 이미지를 개별로 추론하는 기능입니다.</div>
          <br />
          <div>개별로 추론할 이미지를 선택하고 "개별 추론" 버튼을 누릅니다.</div>
          <br />
          <div>(1) 이미지와 CAM 이미지가 나타나며, 추론 결과가 출력됩니다.</div>
        </div>
        <div v-if="status == 2">
          <div>여러 이미지를 추론하는 기능입니다.</div>
          <br />
          <div>(1) 제어단의 버튼을 클릭하여 추론을 진행합니다.</div>
          <br />
          <div>(2) 추론 완료 이미지 테이블에서 항목을 선택하여 좌측 상단에서 결과 이미지를 확인합니다.</div>
          <br />
          <div>로그와 그래프를 통해 추론 진행 상황을 파악합니다.</div>
        </div>
        <div v-if="status == 3">
          <div>(1) "기록" 버튼을 클릭하여 (2) 추론이 완료된 이미지 리스트를 봅니다.</div>
          <br />
          <div>양품과 불량품을 구분하여 리스트를 볼 수 있습니다.</div>
          <br />
          <div>리스트의 항목을 선택하여 이미지의 자세한 내용을 확인합니다.</div>
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
