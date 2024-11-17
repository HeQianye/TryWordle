<template>
  <div class="word-cards">
    <a-card v-for="word in words" :key="word.wordId" :title="word.headWord">
      <a-row>
        <a-col :span="12">
          <strong>词义:</strong>
          <ul>
            <li v-for="(trans, index) in word.content.word" :key="index">{{ trans.tranCn }}</li>
          </ul>
        </a-col>
      </a-row>
    </a-card>
  </div>
</template>

<script>
import { Card, Row, Col } from 'ant-design-vue';

export default {
  components: {
    ACard: Card,
    ARow: Row,
    ACol: Col,
  },
  data() {
    return {
      words: [
        // 这里可以动态加载数据，示例数据如下
        {
          wordRank: 1,
          headWord: "refuse",
          content: {
            word: {
              wordHead: "refuse",
              wordId: "CET4luan_2_1",
              content: {
                sentence: {
                  sentences: [
                    { sContent: "She asked him to leave, but he refused.", sCn: "她叫他走，但他不肯。" },
                    { sContent: "When he offered all that money, I could hardly refuse (= could not refuse ), could I?", sCn: "他愿意给那么多钱，我怎么可能拒绝呢？" }
                  ]
                },
                trans: [
                  { tranCn: "拒绝", pos: "v", tranOther: "to say firmly that you will not do something that someone has asked you to do" }
                ]
              }
            }
          }
        },
      ]
    };
  }
};
</script>

<style scoped>
.word-cards .ant-card {
  margin-bottom: 16px;
}
</style>
