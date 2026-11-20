### 바꾼 내용
`packaging.markers.Marker`에 마커 표현식에서 사용되는 모든 `extra` 이름(정규화됨)을 모아서 돌려주는 `referenced_extras()` 메서드와 헬퍼 함수 `_collect_referenced_extras()`를 추가했다. 
`packaging.requirements.Requirement`에 해당 마커의 extra 이름을 반환하는 `marker_extras` property를 추가했다.
타입ヒント용 `NormalizedName` import도 양쪽 모듈에 모두 반영했다.