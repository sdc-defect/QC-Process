# Docker 명령어
### 도커 이미지
- 이미지 목록
  - docker images
- 이미지 빌드
  - docker build -t {image_name} {dir}
  - ex) docker build -t sdc .
- 특정 이미지 삭제
  - docker rmi {image_name}
- Dangling 이미지 삭제
  - docker image prune
### 도커 컨테이너
- 컨테이너 목록 확인
  - docker ps
  - docker ps -a
- 특정 컨테이너 시작/중지
  - docker start {container_name}
  - docker stop {container_name}
- 특정 컨테이너 강제 삭제
  - docker rm -f {container_name}
- 컨테이너 생성 옵션 및 예시
  - -d : 백그라운드 실행 / -it : 바로 컨테이너 진입
  - -p : 호스트 port와 컨테이너의 port 연결
  - -v : 호스트 폴더와 컨테이너의 폴더 마운트(연결)
  - docker run -d --name {container_name} -p {host_port}:{container_port} -v {host_dir}:{container_dir} {image}:{tag}
  - ex) docker run -d --name sdc -p 8080:8080 -v /home/ubuntu/sdc/log:/app/log sdc:latest