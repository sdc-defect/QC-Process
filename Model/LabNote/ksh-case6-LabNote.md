# ksh-case6-LabNote

<table style="border: 2px; text-align:center;">
  <tr style="font-weight: bold;, font-size: 30px;">
    <td> 제목 </td>
    <td> 내용 </td>
  </tr>
  <tr>
    <td> 모델 요약 (ex. 블록 개수, 구조 등) </td>
    <td> <img src="image/ksh-2022-10-30-mymodel3-B0.jpg"> </td>
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
    <td> 800 </td>
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
    <td> 0.0974 </td>
  </tr>
  <tr>
    <td> Test Loss </td>
    <td> 0.0472 </td>
  </tr>
  <tr>
    <td> Train accuracy / recall / F1-Score </td>
    <td> 0.9977 / 0.9974 / 0.9980 </td>
  </tr>
  <tr>
    <td> Test accuracy / recall / F1-Score </td>
    <td> 0.9769 / 0.9589 / 0.9790 </td>
  </tr>
  <tr>
    <td> val2_cnt (total 50) </td>
    <td> 48 </td>
  </tr>
  <tr>
    <td> must_cnt (total 10) </td>
    <td> 10 </td>
  </tr>
</table>





이전 실험과 다른 점 : decay steps 1200 -> 800 변경

결론 : decay steps 줄어들면서 전체적으로 성능이 떨어진 것 같다. 600 / 1000 으로도 나중에 돌려보면서 비교해볼 예정

