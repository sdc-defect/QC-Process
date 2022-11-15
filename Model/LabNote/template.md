<h1 id="title">{user}-{case}-LabNote</h1>

<table style="border: 2px; text-align:center;">
  <tr style="font-weight: bold;, font-size: 30px;">
    <td> 제목 </td>
    <td> 내용 </td>
  </tr>
  <tr>
    <td> 모델 요약 (ex. 블록 개수, 구조 등) </td>
    <td> <img id="model" src="image/image-20221030115827888.png"> </td>
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
    <td id="init-lr"> {init-lr} </td>
  </tr>
  <tr>
    <td> decay steps </td>
    <td id="decay-steps"> {decay-steps} </td>
  </tr>
  <tr>
    <td> batch size </td>
    <td id="batch-size"> {batch-size} </td>
  </tr>
  <tr>
    <td> epoch </td>
    <td id="epoch"> {epoch} </td>
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
    <td id="train-loss"> {train-loss} </td>
  </tr>
  <tr>
    <td> Test Loss </td>
    <td id="test-loss"> {test-loss} </td>
  </tr>
  <tr>
    <td> Train accuracy / recall / F1-Score </td>
    <td id="train-score"> {acc} / {recall} / {f1} </td>
  </tr>
  <tr>
    <td> Test accuracy / recall / F1-Score </td>
    <td id="test-score"> {acc} / {recall} / {f1} </td>
  </tr>
  <tr>
    <td> val2_cnt (total 50) </td>
    <td id="val2-cnt"> {val2-cnt} </td>
  </tr>
  <tr>
    <td> must_cnt (total 10) </td>
    <td id="must-cnt"> {must-cnt} </td>
  </tr>
</table>



이전 실험과 다른 점 : {...}

결론 : {...}