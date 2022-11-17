# hsd-case7-LabNote

<table style="border: 2px; text-align:center;">
  <tr style="font-weight: bold;, font-size: 30px;">
    <td> 제목 </td>
    <td> 내용 </td>
  </tr>
  <tr>
    <td> 모델 요약 (ex. 블록 개수, 구조 등) </td>
    <td> <img src="image/hsd-image-20221030-mymodel2.png"> </td>
  </tr>
  <tr>
    <td> optimizer </td>
    <td> Adam </td>
  </tr>
  <tr>
    <td> scheduler </td>
    <td> CosineDecayRestarts </td>
  </tr>
  <tr>
    <td> init learning rate </td>
    <td> 0.001 </td>
  </tr>
  <tr>
    <td> decay steps </td>
    <td> 1000 </td>
  </tr>
  <tr>
    <td> batch size </td>
    <td> 16 </td>
  </tr>
  <tr>
    <td> epoch </td>
    <td> 100 </td>
  </tr>
  <tr>
    <td> GPU 여부 (O / X) </td>
    <td> O </td>
  </tr>
  <tr>
    <td> loss function </td>
    <td> CategoricalCrossentropy </td>
  </tr>
  <tr>
    <td colspan="2" style="font-weight: bold;, font-size: 30px;"> best model </td>
  </tr>
  <tr>
    <td> Train Loss </td>
    <td> 0.1614 </td>
  </tr>
  <tr>
    <td> Test Loss </td>
    <td> 0.7501 </td>
  </tr>
  <tr>
    <td> Train accuracy / recall / F1-Score </td>
    <td> 0.9494 / 0.9443 / 0.9558 </td>
  </tr>
  <tr>
    <td> Test accuracy / recall / F1-Score </td>
    <td> 0.5615 / 1.0000 / 0.7192 </td>
  </tr>
  <tr>
    <td> val2_cnt (total 50) </td>
    <td> 50 </td>
  </tr>
  <tr>
    <td> must_cnt (total 10) </td>
    <td> 10 </td>
  </tr>
</table>



이전 실험과 다른 점 : decay-steps 800 -> 1000

결론: Test Loss가  0.0277 -> 0.7501로 확 튀었다. decay-steps는 800으로 고정해야겠다. 혹시 모르니 1200도 테스트