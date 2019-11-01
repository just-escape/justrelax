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
import store from '@/store/store.js'

export default {
  name: 'InventaryPuzzle',
  components: {
    DraggableBlock,
    TableBox,
  },
  data: function() {
    return {
      shadowWidth: 10,
    }
  },
  computed: {
    blocks: function() {
      return store.state.blocks
    },
    blockHeight: function() {
      return store.state.tableHeight / store.state.articles[0].length
    },
    blockWidth: function() {
      return store.state.tableWidth / store.state.articles[0].length
    },
    articles: function() {
      return store.state.articles
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
