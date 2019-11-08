<template>
  <div>
    <div class="position-relative">
      <DraggableBlock
        v-for="(block, blockId) in blocks"
        :key="block.id"
        :id="blockId"
        :left="block.left"
        :top="block.top"
        :width="block.width"
        :height="block.height"
        :color="block.color"
        :backgroundPosition="block.backgroundPosition"
        :zIndex="block.zIndex"
        :shadowWidth="shadowWidth"
      />
      <table>
        <thead>
        </thead>
        <tbody>
          <tr v-for="row in articles" :key="row.id">
            <td v-for="food in row" :key="food.id" :style="{height: blockHeight + 'px', width: blockWidth + 'px'}">
              <TableBox :name="food.name"/>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import DraggableBlock from '@/components/DraggableBlock.vue'
import TableBox from '@/components/TableBox.vue'
import blockStore from '@/store/blockStore.js'

export default {
  name: 'InventoryPuzzle',
  components: {
    DraggableBlock,
    TableBox,
  },
  data: function() {
    return {
      shadowWidth: 10,
      articles: [
        [{name: "apple"}, {name: "orange"}, {name: "grapes"}, {name: "leek"}, {name: "grapes"}, {name: "leek"}],
        [{name: "pear"}, {name: "lemon"}, {name: "strawberry"}, {name: "fish"}, {name: "grapes"}, {name: "leek"}],
        [{name: "protob"}, {name: "rice"}, {name: "water"}, {name: "grains"}, {name: "grapes"}, {name: "leek"}],
        [{name: "powder"}, {name: "pill"}, {name: "milk"}, {name: "coffee"}, {name: "grapes"}, {name: "leek"}],
        [{name: "protob"}, {name: "rice"}, {name: "water"}, {name: "grains"}, {name: "grapes"}, {name: "leek"}],
        [{name: "powder"}, {name: "pill"}, {name: "milk"}, {name: "coffee"}, {name: "grapes"}, {name: "leek"}],
      ]
    }
  },
  computed: {
    blocks: function() {
      return blockStore.state.blocks
    },
    blockHeight: function() {
      return blockStore.state.tableHeight / this.articles.length
    },
    blockWidth: function() {
      return blockStore.state.tableWidth / this.articles.length
    },
  },
  mounted: function() {
    this.$anime.timeline({
      targets: this,
      duration: 3000,
      loop: true,
      easing: 'easeOutCubic',
    }).add({
      shadowWidth: 25,
    }).add({
      shadowWidth: 15,
    })
  },
}
</script>

<style scoped>
table tr td {
  background-color: transparent;
  border: 6px solid transparent;
  line-height: 14px;
  font-size: 12px;
}
</style>
