<template>
  <div class="position-relative" :style="{'height': height + 'px', 'width': width + 'px'}">
    <InventaryPuzzle class="puzzle"/>
    <LeftMenu class="left-menu"/>
    <BottomFrame class="bottom-frame"/>
  </div>
</template>

<script>
import InventaryPuzzle from '@/components/InventaryPuzzle.vue'
import LeftMenu from '@/components/LeftMenu.vue'
import BottomFrame from '@/components/BottomFrame.vue'
import store from '@/store/store.js'

export default {
  name: 'Container',
  components: {
    InventaryPuzzle,
    LeftMenu,
    BottomFrame,
  },
  computed: {
    height: function() {
      // 6 is the margin
      return store.state.tableHeight + 50 + 6
    },
    width: function() {
      // 6 is the margin
      return store.state.tableWidth + 300 + 6
    },
  },
}
</script>

<style scoped>
.puzzle {
  position: absolute;
  top: 0;
  right: 0;
}

.left-menu {
  position: absolute;
  top: 0;
  left: 0;
  width: 300px;
  height: 100%;
}

.bottom-frame {
  position: absolute;
  bottom: 0;
  right: 0;
  height: 50px;
}
</style>
