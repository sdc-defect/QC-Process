# kmy-case8-LabNote

<table style="border: 2px; text-align:center;">
  <tr style="font-weight: bold;, font-size: 30px;">
    <td> 제목 </td>
    <td> 내용 </td>
  </tr>
  <tr>
    <td> 모델 요약 (ex. 블록 개수, 구조 등) </td>
    <td> <img src="image/kmy-image.png"> </td>
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
    <td> 0.0001 </td>
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
    <td> 0.04938905 </td>
  </tr>
  <tr>
    <td> Test Loss </td>
    <td> 0.14238313 </td>
  </tr>
  <tr>
    <td> Train accuracy / recall / F1-Score </td>
    <td> 0.999834656084656 / 0.999723298284449 / 0.999861629998616 </td>
  </tr>
  <tr>
    <td> Test accuracy / recall / F1-Score </td>
    <td> 1.0 / 1.0 / 1.0 </td>
  </tr>
  <tr>
    <td> val2_cnt (total 50) </td>
    <td> 48 </td>
  </tr>
  <tr>
    <td> must_cnt (total 10) </td>
    <td>  </td>
  </tr>
</table>





이전 실험과 다른 점 : 학습률 감소 (0.0005 -> 0.0001)

결론 : test loss 두 배 이상 증가

