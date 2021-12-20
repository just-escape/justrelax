<template>
  <div class="w-100">
    <div class="border-deepdark rounded p-3 mb-3">
        <div class="d-flex flex-row align-items-center">
            <div class="d-flex flex-column w-100">
                <div class="d-flex flex-row justify-content-around flex-grow-1 mb-4">
                    <div class="d-flex flex-column justify-content-center">
                        <div class="d-flex justify-content-center">
                            <div class="jack-port mb-1"></div>
                        </div>
                        <div>branché</div>
                    </div>
                    <div class="d-flex flex-column justify-content-center">
                        <div class="d-flex justify-content-center">
                            <div class="jack-port mb-1"></div>
                        </div>
                        <div>débranché</div>
                    </div>
                </div>
                <div class="d-flex flex-row justify-content-between ml-4 mr-5">
                    <div class="d-flex flex-column">
                        <div class="d-flex flex-row mb-2">
                            <div class="mr-2" style="height: 20px; width: 20px" :style="{background: '#dc3545'}"></div>
                            <div style="line-height: 20px">Lumières</div>
                        </div>
                        <div class="d-flex flex-row">
                            <div class="mr-2" style="height: 20px; width: 20px" :style="{background: '#dc3545'}"></div>
                            <div style="line-height: 20px">Menu</div>
                        </div>
                    </div>
                    <div class="d-flex flex-column justify-content-center">
                        <div class="table-button"></div>
                    </div>
                </div>
            </div>
            <div>
                <div style="height: 20px; width: 20px" :style="{background: '#dc3545'}"></div>
            </div>
        </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "WidgetControlPanel",
  components: {

  },
  props: [
    "defaultChannel",
    "row",
    "roomId",
  ]
}
</script>

<style scoped>
.jack-port {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 6px #2e2e2e solid;
  background: lightgrey;
}
.table-button {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 3px lightgrey solid;
  background: #2e2e2e;
}
</style>