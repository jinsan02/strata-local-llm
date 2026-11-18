수정을 마쳤다. 무엇을 바꿨는지 짧게 답하고 끝내라.

src/flask/blueprints.py에서 `Blueprint.__init__` 메서드의 `name` 파라미터 유효성 검사 부분을 수정했습니다. 빈 문자열 또는 None이 전달되면 `ValueError("Blueprint name may not be empty.")` 예외를 발생시키도록 했습니다. 기존에 "." 문자 체크 전에 추가했습니다.