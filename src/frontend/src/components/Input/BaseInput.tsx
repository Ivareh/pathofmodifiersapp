import { Flex } from "@chakra-ui/layout";
import { useState } from "react";
import { Checkbox, CheckboxIcon, Text } from "@chakra-ui/react";
import { BaseTypeInput } from "./ItemBaseTypeInputComp/BaseTypeInput";
import { useQueryClient } from "@tanstack/react-query";
import {
  BaseType,
  ItemBaseTypeCategory,
  ItemBaseTypeSubCategory,
  ItemBaseTypesService,
} from "../../client";
import { CategoryInput } from "./ItemBaseTypeInputComp/CategoryInput";
import { SubCategoryInput } from "./ItemBaseTypeInputComp/SubCategoryInput";

export const BaseInput = () => {
  const [baseExpanded, setBaseExpanded] = useState(false);
  const [baseTypes, setBaseTypes] = useState<BaseType | BaseType[]>([]);
  const [itemBaseTypeCategory, setItemBaseTypeCategory] = useState<
    ItemBaseTypeCategory | ItemBaseTypeCategory[]
  >([]);
  const [itemBaseTypeSubCategory, setItemBaseTypeSubCategory] = useState<
    ItemBaseTypeSubCategory | ItemBaseTypeSubCategory[]
  >([]);

  const queryClient = useQueryClient();

  const handleExpanded = () => {
    console.log("EXPANDED");
    setBaseExpanded(!baseExpanded);
  };

  const prefetchAllBaseTypeData = async () => {
    await queryClient.prefetchQuery({
      queryKey: ["baseTypes"],
      queryFn: async () => {
        setBaseTypes(
          await ItemBaseTypesService.getBaseTypesApiApiV1ItemBaseTypeBaseTypesGet()
        );
      },
      staleTime: 10 * 1000, // only prefetch if older than 10 seconds
    });

    await queryClient.prefetchQuery({
      queryKey: ["itemBaseTypeCategory"],
      queryFn: async () => {
        setItemBaseTypeCategory(
          await ItemBaseTypesService.getUniqueCategoriesApiApiV1ItemBaseTypeUniqueCategoriesGet()
        );
      },
      staleTime: 10 * 1000, // only prefetch if older than 10 seconds
    });

    await queryClient.prefetchQuery({
      queryKey: ["itemBaseTypeSubCategory"],
      queryFn: async () => {
        setItemBaseTypeSubCategory(
          await ItemBaseTypesService.getUniqueSubCategoriesApiApiV1ItemBaseTypeUniqueSubCategoriesGet()
        );
      },
      staleTime: 10 * 1000, // only prefetch if older than 10 seconds
    });
  };

  return (
    <Flex direction={"column"}>
      <Flex>
        <Checkbox
          onChange={handleExpanded}
          onMouseEnter={async () => {
            prefetchAllBaseTypeData()
          }}
        >
          <CheckboxIcon />
        </Checkbox>
        <Text color={"ui.white"}>Base type</Text>
      </Flex>
      {baseExpanded && (
        <Flex flexWrap={"wrap"} width={650}>
          <BaseTypeInput baseTypes={baseTypes} />
          <CategoryInput categories={itemBaseTypeCategory} />
          <SubCategoryInput subCategories={itemBaseTypeSubCategory} />
        </Flex>
      )}
    </Flex>
  );
};
