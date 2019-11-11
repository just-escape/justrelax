<template>
  <div class="row">
    <div
      v-for="category in admin.categories"
      :key="category.id"
      class="col-3 mb-4"
    >
      <PageEditorAdminCard :category="category"/>
    </div>
  </div>
</template>

<script>
import PageEditorAdminCard from '@/components/PageEditorAdminCard.vue'
import rulesStore from '@/store/rulesStore.js'

export default {
  name: 'PageEditorAdmin',
  components: {
    PageEditorAdminCard,
  },
  computed: {
    admin: function() {
      return rulesStore.state.admin
    }
  },
}
</script>
