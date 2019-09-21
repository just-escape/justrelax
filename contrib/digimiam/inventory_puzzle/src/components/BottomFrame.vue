<template>
  <div class="frame">
    <div class="bottom-right-corner"></div>
    <div class="content h-100"></div>
  </div>
</template>

<style scoped>
.frame {
  padding: 5px;
  z-index: 10;
  width: calc(100% - 300px + 10px + 3px);
}

.content {
  border: 3px solid #00d1b6;
  box-shadow: 0px 0px 14px -6px rgba(0, 209, 182, 1);
  background-color: rgba(00, 45, 64, 0.5);
  color: #ffffff;
}

.bottom-right-corner {
  position: absolute;
  bottom: 5px;
  right: 5px;
  display: block;
  border: 10px solid #00d1b6;
  border-left-color: transparent;
  border-top-color: transparent;
}
</style>
