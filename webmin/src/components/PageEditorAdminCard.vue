<template>
  <b-card
    :header="category.name"
    header-tag="h3"
    header-class="big-noodle text-jaffa text-center"
    class="bgc-dark border-jaffa h-100"
  >
    <ul>
      <li v-for="subcat in category.subcategories" :key="subcat.id">
        {{ subcat.name }}
        <ul>
          <li v-for="action in subcat.actions" :key="action.id">
            {{ action.name }} - {{ action.icon }}
          </li>
        </ul>
      </li>
    </ul>
  </b-card>
</template>

<script>
export default {
  name: 'PageEditorAdminCard',
  props: ['category'],
}
</script>
