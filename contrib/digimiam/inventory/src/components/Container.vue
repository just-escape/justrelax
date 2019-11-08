<template>
  <div class="position-relative" :style="{'height': height + 'px', 'width': width + 'px'}">
    <InventoryPuzzle class="puzzle"/>
    <LeftMenu class="left-menu"/>
    <div class="main-frame"></div>
    <div class="main-frame-background"></div>
  </div>
</template>

<script>
import InventoryPuzzle from '@/components/InventoryPuzzle.vue'
import LeftMenu from '@/components/LeftMenu.vue'
import blockStore from '@/store/blockStore.js'

export default {
  name: 'Container',
  components: {
    InventoryPuzzle,
    LeftMenu,
  },
  computed: {
    height: function() {
      // 6 is the margin
      return blockStore.state.tableHeight + 50 + 6
    },
    width: function() {
      // 6 is the margin
      return blockStore.state.tableWidth + 300 + 6
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

.main-frame {
  position: absolute;
  bottom: 5px;
  right: 5px;
  top: 5px;
  left: 5px;
  z-index: 20;
  filter: drop-shadow(0px 0px 2px rgba(0, 209, 182, 0.75));
  clip-path: polygon(
    calc(290px - 3px) -4px,
    calc(290px + 4px) -4px,
    calc(290px + 4px) calc(100% - 40px - 4px),
    calc(100% + 4px) calc(100% - 40px - 4px),
    calc(100% + 4px) calc(100% - (20px - 2px)),
    calc(100% - (20px - 2px)) calc(100% + 8px),
    calc(40px - 2px) calc(100% + 8px),
    -8px calc(100% - 40px + 2px),
    -8px calc(40px - 8px),
    calc(40px - 8px) -4px,
    calc(290px - 3px) -4px,
    calc(290px - 3px) 9px,
    calc(40px - 2px) 9px,
    3px calc(40px + 2px),
    3px calc(100% - 40px),
    calc(40px) calc(100% - 3px),
    calc(100% - 20px) calc(100% - 3px),
    calc(100% - 3px) calc(100% - 20px),
    calc(100% - 3px) calc(100% - 40px + 3px),
    calc(290px - 3px) calc(100% - 40px + 3px)
  );
}

.main-frame::before {
  content: '';
  position: absolute;
  background-color: #00d1b6;
  bottom: 0;
  right: 0;
  left: 0;
  top: 0;
  z-index: 20;
  clip-path: polygon(
    calc(290px - 3px) 0%,
    290px 0%,
    290px calc(100% - 40px),
    100% calc(100% - 40px),
    100% calc(100% - (20px - 2px)),
    calc(100% - (20px - 2px)) 100%,
    calc(40px - 2px) 100%,
    0% calc(100% - 40px + 2px),
    0% 40px,
    40px 0%,
    calc(290px - 3px) 0%,
    calc(290px - 3px) 9px,
    calc(40px - 2px) 9px,
    3px calc(40px + 2px),
    3px calc(100% - 40px),
    calc(40px) calc(100% - 3px),
    calc(100% - 20px) calc(100% - 3px),
    calc(100% - 3px) calc(100% - 20px),
    calc(100% - 3px) calc(100% - 40px + 3px),
    calc(290px - 3px) calc(100% - 40px + 3px)
  );
}

.main-frame-background {
  position: absolute;
  bottom: 5px;
  right: 5px;
  top: 5px;
  left: 5px;
  background-color: rgba(0, 45, 64, 0.5);
  clip-path: polygon(
    40px 0%,
    290px 0%,
    290px calc(100% - 40px),
    100% calc(100% - 40px),
    100% calc(100% - 20px),
    calc(100% - 20px) 100%,
    40px 100%,
    0% calc(100% - 40px),
    0% 40px
  );
  z-index: 0;
}
</style>
