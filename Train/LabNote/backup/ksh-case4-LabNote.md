# ksh-case4-LabNote

<table style="border: 2px; text-align:center;">
  <tr style="font-weight: bold;, font-size: 30px;">
    <td> 제목 </td>
    <td> 내용 </td>
  </tr>
  <tr>
    <td> 모델 요약 (ex. 블록 개수, 구조 등) </td>
    <td> <img src="image/ksh-2022-10-30-mymodel3-B2.jpg"> </td>
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
    <td> 0.0005 </td>
  </tr>
  <tr>
    <td> decay steps </td>
    <td> 1200 </td>
  </tr>
  <tr>
    <td> batch size </td>
    <td> 16 </td>
  </tr>
  <tr>
    <td> epoch </td>
    <td> 50 </td>
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
    <td> 0.0857 </td>
  </tr>
  <tr>
    <td> Test Loss </td>
    <td> 0.0530 </td>
  </tr>
  <tr>
    <td> Train accuracy / recall / F1-Score </td>
    <td> 0.9990 / 0.9983 / 0.9986 </td>
  </tr>
  <tr>
    <td> Test accuracy / recall / F1-Score </td>
    <td> 0.9769 / 0.9589 / 0.9790 </td>
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



이전 실험과 다른 점 : EfficientNet V2 B1 => B2 모델로 변경

결론 : 동일 조건에서 꼭 잡아야 하는 불량에 대해서는 B2가 성능이 좋은데, train / test 모두 loss / accuracy / recall / f1-score 는 B1이 더 나은 것 같다. 다른 조건으로도 실험 필요할 것 같다.

